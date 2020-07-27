from dotenv import load_dotenv
from app import create_app, db
from sqlalchemy import inspect

load_dotenv()
app = create_app()

from app.models import URL, User, Visit

with app.app_context():
  tables_created = len(inspect(db.engine).get_table_names())
  if (tables_created and len(User.query.all()) == 0):
    # add guest as default user if database does not contain one
    guest = User().set_value(name='guest', username='guest@shortify.com', email='guest@shortify.com', password='password')
    db.session.add(guest)
    db.session.commit()
    print('Guest user is created')


@app.shell_context_processor
def make_shell_context():
  return {'db': db, 'URL': URL, 'User': User, 'Visit': Visit}