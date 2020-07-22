from dotenv import load_dotenv
load_dotenv()
from app import app, db
from app.models import URL, User

@app.shell_context_processor
def make_shell_context():
  return {'db': db, 'URL': URL, 'User': User}