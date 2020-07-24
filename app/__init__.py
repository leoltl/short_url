from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment


login = LoginManager()
login.login_view = 'login'
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()

def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(Config)

  db.init_app(app)
  migrate.init_app(app)
  moment.init_app(app)
  login.init_app(app)

  return app

app = create_app(Config)

from app import routes, errors, models