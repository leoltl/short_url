from app import db
from app.models import Visit, URL
from app.main import bp
from app.main.forms import MainURLForm
from app.geolocation import locate
from flask import render_template, flash, redirect, url_for, request, current_app
from utils import retry
from flask_login import current_user, login_required
from sqlalchemy import exc

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
  form = MainURLForm()
  return render_template('index.html', form=form)

@bp.route('/result', methods=['GET', 'POST'])
def result():
  if request.args.get('short'):
    urlID = request.args.get('short')
    url = URL.query.filter_by(short=urlID).first_or_404(
      description=f'There is no data with {urlID}')
    return render_template('short_url.html', url=url, title='Shortened URL')

  shortID, urlObject = None, None
  def insertURL(url):
    nonlocal shortID, urlObject
    urlObject, shortID = URL().set_value(
      full=url, 
      userid=current_user.id if current_user.is_authenticated else 1)
    db.session.add(urlObject)
    db.session.commit()

  form = MainURLForm(request.form)
  if form.validate_on_submit():
    try:
      insertURL(form.fullUrl.data)
    except exc.IntegrityError:
      db.session.rollback()
      retry(lambda: insertURL(form.fullUrl.data), 2)
    return redirect(url_for('main.result', short=[shortID]))
  return redirect(url_for('main.index'))

@bp.route('/l/<shortID>')
def redirect_to_full(shortID):
  def record_visit(url):
    visit = Visit(url_record=url)
    db.session.add(visit)
    db.session.commit()
    ip = request.remote_addr
    if not ip or (not current_app.debug and ip == '127.0.0.1'):
      return
    locate(request.remote_addr, visit.id)

  url = URL.query.filter_by(short=shortID).first_or_404(
    description=f'There is no data with {shortID}')
  if url.is_disabled:
    flash('Sorry, URL you requested is disabled by the owner')
    # TODO send to proper page to handle disabled url
    return redirect('404')
  record_visit(url.id)
  return redirect(url.full)

@bp.route('/dashboard')
@login_required
def dashboard():
  urls = current_user.urls.all()
  return render_template('dashboard.html', urls=urls, title='Dashboard')