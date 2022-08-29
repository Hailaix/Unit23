"""Seed users table in blogly database"""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# add users
anyone = User(first_name="Alfred", last_name="Anyone")
someone = User(first_name="Somebody", last_name="Important")
noone = User(first_name="Nobody", last_name="Important")

# Add new objects to session, so they'll persist
db.session.add(anyone)
db.session.add(someone)
db.session.add(noone)

# Commit--otherwise, this never gets saved!
db.session.commit()
