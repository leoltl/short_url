from app import db, app, login
from werkzeug.security import generate_password_hash, check_password_hash
from utils import generateUniqueID
from datetime import datetime
from flask_login import UserMixin

shortUrl_length = app.config['SHORTURL_LENGTH']

class URL(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=1)
  full = db.Column(db.String(512))
  short = db.Column(
    db.String(shortUrl_length), 
    index=True,
    unique=True)
  create_at=db.Column(
    db.DateTime,
    default=datetime.utcnow)

  def __repr__(self):
    return f'<URL {self.full} - {self.id}>'

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255))
  username = db.Column(
    db.String(255), 
    index=True, 
    unique=True)
  email = db.Column(
    db.String(255), 
    index=True, 
    unique=True)
  password_hash = db.Column(db.String(128))
  urls = db.relationship('URL', backref='owner', lazy='dynamic')

  def __repr__(self):
    return f'<User {self.name}:{self.email}>'

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
  return User.query.get(id)