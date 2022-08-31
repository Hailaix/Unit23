"""Seed users table in blogly database"""

from models import User, db, Post, Tag
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()
Tag.query.delete()

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

p1 = Post(title="Is anyone here?", content="haha, just kidding, I'm anyone", user_id=anyone.id)
p2 = Post(title="Post 2", content="This is a post by somebody", user_id=someone.id)
p3 = Post(title="Somebody is a prolific poster", 
            content="Somebody has a lot of time to be posting things", user_id=someone.id)

db.session.add(p1)
db.session.add(p2)
db.session.add(p3)
db.session.commit()