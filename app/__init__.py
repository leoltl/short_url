from flask import Flask, current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_mail import Mail

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
migrate = Migrate()
moment = Moment()
mail = Mail()

def create_app(config_class=Config):

  app = Flask(__name__)
  app.config.from_object(Config)

  db.init_app(app)
  migrate.init_app(app, db)
  moment.init_app(app)
  login.init_app(app)
  mail.init_app(app)

  with app.app_context():
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app import models

  return app