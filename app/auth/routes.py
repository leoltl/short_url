from app import db
from app.models import User
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from functools import wraps

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

@bp.route('/login', methods=('GET', 'POST'))
@login_disallowed
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if not user or not user.check_password(form.password.data):
      flash('Invalid username or password')
      return redirect(url_for('auth.login'))
    login_user(user, remember=form.remember_me.data)
    flash(f'Welcome, {user.name}')
    next_page = request.args.get('next')
    return redirect(next_page if next_page and url_parse(next_page).netloc == '' else url_for('main.index'))
  return render_template('auth/login.html', form=form, title='Sign in')

@bp.route('/logout')
def logout():
  logout_user()
  flash('You have successfully logged out.')
  return redirect(url_for('main.index'))

@bp.route('/register', methods=('GET', 'POST'))
@login_disallowed
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User().set_value(
      name=form.name.data, 
      email=form.email.data, 
      username=form.email.data,
      password=form.password.data)
    db.session.add(user)
    db.session.commit()
    login_user(user, remember=True)
    return redirect(url_for('main.index'))
  return render_template('auth/register.html', form=form, title='Sign up')

@bp.route('/reset_password')
def reset_password_request():
  pass