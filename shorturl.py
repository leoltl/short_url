from dotenv import load_dotenv
load_dotenv()
from app import app, db
from app.models import URL, User, Visit

if (len(User.query.all()) == 0):
  # add guest as default user if database does not contain one
  guest = User().set_value(name='guest', username='guest@shortify.com', email='guest@shortify.com', password='password')
  db.session.add(guest)
  db.session.commit()
  print("Guest user is created")

@app.shell_context_processor
def make_shell_context():
  return {'db': db, 'URL': URL, 'User': User, 'Visit': Visit}