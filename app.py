"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secretblogly"
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def index():
    """(temp) redirects to users page"""
    return redirect("/users")


# Part 1 Routes ------------------------------------------------------------------
@app.route("/users")
def users():
    """displays all users"""
    users = User.query.order_by(User.last_name.asc(),User.first_name.asc()).all()
    return render_template("users.html", users=users)

@app.route("/users/new")
def userform():
    """form page to create a new user"""
    return render_template("userform.html")

@app.route("/users/new", methods=["POST"])
def userform_submit():
    """create a new user on submit of new user form"""
    first_name = request.form["first_name"].strip()
    last_name = request.form["last_name"].strip()
    image_url = request.form["image_url"].strip()
    if not image_url:
        image_url = None
    newuser = User(first_name=first_name,last_name=last_name,image_url=image_url)
    db.session.add(newuser)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>")
def user_details(user_id):
    """Shows the details of the user with id user_id"""

    curruser = User.query.get_or_404(user_id)
    return render_template("userpage.html", user=curruser)

@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """edit the details of the user with id user_id"""

    curruser = User.query.get_or_404(user_id)
    return render_template("usereditform.html",user=curruser)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user_submit(user_id):
    """edits the details of user with id user_id"""
    new_fname = request.form["first_name"].strip()
    new_lname = request.form["last_name"].strip()
    new_img_url = request.form["image_url"].strip()
    
    curruser = User.query.get_or_404(user_id)
    
    if new_fname:
        curruser.first_name = new_fname
    if new_lname:
        curruser.last_name = new_lname
    if new_img_url:
        curruser.image_url = new_img_url
        
    db.session.add(curruser)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """delete the user with id user_id"""
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect("/users")
# --------------------------------------------------------------------------------

# Part 2 Routes ------------------------------------------------------------------

@app.route("/users/<int:user_id>/posts/new")
def postform(user_id):
    """creates a new post posted by the user with id user_id"""
    user = User.query.get_or_404(user_id)
    return render_template("postform.html", user=user)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def postform_submit(user_id):
    """Creates new post on POST and redirects back to user page"""
    post_title = request.form["title"].strip()
    post_content = request.form["content"].strip()
    new_post = Post(title=post_title, content=post_content, user_id=user_id)

    db.session.add(new_post)
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def post_details(post_id):
    """show details of post with id post_id"""
    post = Post.query.get_or_404(post_id)
    return render_template("postpage.html", post=post)

@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """edit the details of post with id post_id"""
    post = Post.query.get_or_404(post_id)
    return render_template("posteditform.html", post=post)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post_submit(post_id):
    """edit post on post and redirects back to post page"""
    new_title = request.form["title"].strip()
    new_content = request.form["content"].strip()

    post = Post.query.get_or_404(post_id)

    if new_title:
        post.title = new_title
    if new_content:
        post.content = new_content

    db.session.add(post)
    db.session.commit()
    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """delete post with id post_id"""
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect("/")
# --------------------------------------------------------------------------------