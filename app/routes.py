from app import app, db
from app.models import URL, User
from app.forms import MainURLForm, LoginForm, RegistrationForm
from flask import render_template, flash, redirect, url_for, request, session
from utils import generateUniqueID, retry
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import timedelta 
from functools import wraps
import json 

shortUrl_length = app.config['SHORTURL_LENGTH']

def login_disallowed(_fn=None, *, redirect_to=None):
  # prevent signed in user to access specified (ie decorated) route, specify
  # redirect location by provideing route function name to redirect_to
  redirect_to = redirect_to or 'index'
  def _login_disallowed(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
      if current_user.is_authenticated:
        return redirect(url_for(redirect_to))
      return fn(*args, **kwargs)
    return wrapper
  if _fn is None:
    return _login_disallowed
  else :
    return _login_disallowed(_fn)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
  form = MainURLForm()
  return render_template('index.html', form=form)

@app.route('/result', methods=["GET", "POST"])
def result():
  if request.args.get('short'):
    urlID = request.args.get('short')
    url = URL.query.filter_by(short=urlID).first_or_404(
      description=f'There is no data with {urlID}')
    return render_template('short_url.html', url=url, title='Shortened URL')

  shortID = None
  urlObject = None
  def insertURL(url):
    nonlocal shortID
    nonlocal urlObject
    shortID = generateUniqueID(shortUrl_length)
    urlObject = URL(full=url, short=shortID)
    db.session.add(urlObject)
    db.session.commit()
  form = MainURLForm(request.form)
  if form.validate_on_submit():
    try:
      insertURL(form.fullUrl.data)
    except Exception as e:
      db.session.rollback()
      retry(lambda: insertURL(form.fullUrl.data), 2)
    flash(f'Url is successfully shortified {shortID}')
    return redirect(url_for('result', short=[shortID]))
  return redirect(url_for('index'))

@app.route('/l/<shortID>')
def redirect_to_full(shortID):
  url = URL.query.filter_by(short=shortID).first_or_404(
    description=f'There is no data with {shortID}')
  return redirect(url.full)

@app.route('/login', methods=('GET', 'POST'))
@login_disallowed
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if not user or not user.check_password(form.password.data):
      flash('Invalid username or password')
      return redirect(url_for("login"))
    login_user(user, remember=form.remember_me.data)
    flash(f"Welcome, {user.name}")
    next_page = request.args.get('next')
    return redirect(next_page if next_page and url_parse(next_page).netloc == '' else url_for('index'))
  return render_template('login.html', form=form, title="Sign in")

@app.route('/logout')
def logout():
  logout_user()
  flash("You have successfully logged out.")
  return redirect(url_for('index'))

@app.route('/register', methods=('GET', 'POST'))
@login_disallowed
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(
      name=form.name.data, 
      email=form.email.data, 
      username=form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    login_user(user, remember=True)
    return redirect(url_for('index'))
  return render_template('register.html', form=form, title="Sign up")

@app.route('/reset_password')
def reset_password_request():
  pass

