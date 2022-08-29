"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """connect the database to the app"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User database model"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    image_url = db.Column(db.String, nullable=False, default="https://cdn.iconscout.com/icon/free/png-256/user-3114475-2598167.png")