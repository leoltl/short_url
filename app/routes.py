from app import app, db
from app.models import URL, User
from app.forms import MainURLForm
from flask import render_template, flash, redirect, url_for
from utils import generateUniqueID, retry


shortUrl_length = app.config['SHORTURL_LENGTH']

@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
  shortID = None
  def insertURL(url):
    nonlocal shortID 
    shortID = generateUniqueID(shortUrl_length)
    url = URL(full=url, short=shortID)
    db.session.add(url)
    db.session.commit()
  form = MainURLForm()  
  if form.validate_on_submit():
    try:
      insertURL(form.fullUrl.data)
    except Exception as e:
      db.session.rollback()
      retry(lambda: insertURL(form.fullUrl.data), 2)
    flash(f'Url is successfully shortified {shortID}')
    return redirect(url_for('make_short_url', shortID=shortID))
  return render_template('index.html', form=form)

@app.route("/l/<shortID>")
def redirect_to_full(shortID):
  url = URL.query.filter_by(short=shortID).first_or_404(
    description=f'There is no data with {shortID}')
  return redirect(url.full)

@app.route("/result/<shortID>")
def make_short_url(shortID):
  url = URL.query.filter_by(short=shortID).first_or_404(
    description=f'There is no data with {shortID}')
  return render_template('short_url.html', url=url, title="Shortened URL")