from flask import render_template
from app import db
from app.main import bp

@bp.errorhandler(404)
def not_found_error(error=None):
  return render_template("404.html", error=error), 400

@bp.errorhandler(500)
def internal_error(error):
  db.session.rollback()
  return render_template('500.html'), 500