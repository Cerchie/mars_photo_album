"""Seed file to make sample data for db"""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
gemma = User(first_name='Gemma', last_name="Smith")
george = User(first_name='George', last_name="Sanders")
gillian = User(first_name='Gillian', last_name="Sally")

# Add new objects to session, so they'll persist
db.session.add(gemma)
db.session.add(george)
db.session.add(gillian)

# Commit--otherwise, this never gets saved!
db.session.commit()