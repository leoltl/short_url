from flask import Flask, current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'login'
migrate = Migrate()
moment = Moment()

def create_app(config_class=Config):

  app = Flask(__name__)
  app.config.from_object(Config)

  db.init_app(app)
  migrate.init_app(app)
  moment.init_app(app)
  login.init_app(app)

  with app.app_context():
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app import models

  return app