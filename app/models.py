from werkzeug.security import generate_password_hash, check_password_hash
from utils import generateUniqueID
from datetime import datetime
from flask_login import UserMixin
from flask import current_app
from app import db, login
from time import time
import jwt

shortUrl_length = current_app.config['SHORTURL_LENGTH']

class User(UserMixin, db.Model):
  id            = db.Column(db.Integer, primary_key=True)
  name          = db.Column(db.String(255))
  password_hash = db.Column(db.String(128))
  username      = db.Column(
                    db.String(255), 
                    index=True, 
                    unique=True)
  email         = db.Column(
                    db.String(255), 
                    index=True, 
                    unique=True)
  urls          = db.relationship('URL', backref='owner', lazy='dynamic')

  def __repr__(self):
    return f'<User {self.name}:{self.email}>'

  def set_value(self, *, name, email, username, password):
    self.name          = name
    self.email         = email
    self.username      = username
    self.set_password(password)
    return self

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)
  
  def get_reset_password_token(self, exprires_in=600):
    return jwt.encode(
      {'reset_password': self.id, 'exp': time() + exprires_in},
      current_app.config['SECRET_KEY'], algorithm='HS256'
    ).decode('utf-8')
  
  @staticmethod
  def verify_reset_password_token(token):
    try:
      id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms='HS256')['reset_password']
    except:
      return
    return User.query.get(id)

class URL(db.Model):
  id          = db.Column(db.Integer, primary_key=True)
  user_id     = db.Column(db.Integer, db.ForeignKey('user.id'))
  full        = db.Column(db.String(512))
  short       = db.Column(
                  db.String(shortUrl_length), 
                  index=True,
                  unique=True)
  create_at   = db.Column(
                  db.DateTime,
                  default=datetime.utcnow)
  is_disabled = db.Column(
                  db.Boolean,
                  default=False)
  visits      = db.relationship('Visit', backref='url_data', lazy='select')

  def set_value(self, *, full, userid):
    self.full    = self._verify_url(full)
    self.user_id = userid or 1
    self.short   = generateUniqueID(shortUrl_length)
    return (self, self.short)

  def _verify_url(self, full_url):
    return full_url if 'http' in full_url.lower() else f'http://{full_url}'

  def __repr__(self):
    return f'<URL {self.full} - {self.id}>'
  
  def __str__(self):
    return f'URL {self.full} - {self.id}'

class Visit(db.Model):
  id           = db.Column(db.Integer, primary_key=True)
  url_record   = db.Column(db.Integer, db.ForeignKey('URL.id'))
  timestamp    = db.Column(db.DateTime, default=datetime.utcnow)
  ip           = db.Column(db.String(45))
  country_code = db.Column(db.String(2)) #ISO 3166-1 alpha-2 codes
  region_name  = db.Column(db.String(50))
  city_name    = db.Column(db.String(50))
  lat          = db.Column(db.Float())
  lon          = db.Column(db.Float())

  def set_geo_info(self, *, ip, country_code, region_name, city_name, lon, lat):
    self.ip           = ip 
    self.country_code = country_code
    self.region_name  = region_name
    self.city_name    = city_name
    self.lon          = lon
    self.lat          = lat
  
  def __repr__(self):
    return f'<Visit {self.id}>'
  
  def serialize(self):
    return {
      'id'          : self.id,
      'timestamp'   : self.timestamp,
      'ip'          : self.ip ,
      'country_code': self.country_code,
      'region_name' : self.region_name,
      'city_name'   : self.city_name,
      'lon'         : self.lon,
      'lat'         : self.lat
    }



@login.user_loader
def load_user(id):
  return User.query.get(id)