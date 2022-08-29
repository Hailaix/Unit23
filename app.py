"""Blogly application."""

from flask import Flask, render_template, redirect
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secretblogly"
debug = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()

@app.route("/")
def index():
    """(temp) redirects to users page"""
    return redirect("/users")

@app.route("/users")
def users():
    """displays all users"""
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/users/new")
def userform():
    """form page to create a new user"""
    return render_template("userform.html")

@app.route("/users/<int:user_id>")
def user_details(user_id):
    """Shows the details of the user with id user_id"""

    curruser = User.query.get_or_404(user_id)
    return render_template("userpage.html", user=curruser)

