"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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

    # full name property
    def _get_full_name(self):
        """returns the first and last name of the user"""
        return f"{self.first_name} {self.last_name}"

    full_name = property(
        fget=_get_full_name,
        doc="Full name of the user"
    )

class Post(db.Model):
    """Post database model"""
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    #User relationship
    author = db.relationship('User', backref="posts")

    # readable time property
    def _time_read(self):
        """returns created_at in a formatted string"""
        return self.created_at.strftime("%a %b %d %Y, %I:%M %p")
    readable_date = property(
        fget=_time_read,
        doc="returns created_at in a readable format"
    )

class Tag(db.Model):
    """Tag database model"""
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)

    # "Through" Relationship
    posts = db.relationship('Post', secondary='posts_tags', backref='tags')

class PostTag(db.Model):
    """Many-to-Many between posts and tags"""
    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
