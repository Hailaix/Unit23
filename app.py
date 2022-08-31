"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post, Tag
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
    if not first_name or not last_name or len(first_name) > 32 or len(last_name) > 32:
        if not first_name or len(first_name) > 32:
            flash("First Name must be between 1 and 32 characters","danger")
        if not last_name or len(last_name) > 32:
            flash("Last Name must be between 1 and 32 characters", "danger")
        return redirect("/users/new")
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

    if len(new_fname) > 32 or len(new_lname) > 32:
        if len(new_fname) > 32:
            flash("First Name must be between 1 and 32 characters","danger")
        if len(new_lname) > 32:
            flash("Last Name must be between 1 and 32 characters", "danger")
        return redirect(f"/users/{user_id}/edit")
    
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
    tags = Tag.query.all()
    return render_template("postform.html", user=user, tags=tags)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def postform_submit(user_id):
    """Creates new post on POST and redirects back to user page"""
    post_title = request.form["title"].strip()
    post_content = request.form["content"].strip()
    # post tags handling
    tids = [int(tid) for tid in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tids)).all()

    if post_title:
        new_post = Post(title=post_title, content=post_content, user_id=user_id, tags=tags)

        db.session.add(new_post)
        db.session.commit()
        return redirect(f"/users/{user_id}")
    else:
        flash("Posts must have a Title", "danger")
        return redirect(f"/users/{user_id}/posts/new")

@app.route("/posts/<int:post_id>")
def post_details(post_id):
    """show details of post with id post_id"""
    post = Post.query.get_or_404(post_id)
    return render_template("postpage.html", post=post)

@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """edit the details of post with id post_id"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("posteditform.html", post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post_submit(post_id):
    """edit post on post and redirects back to post page"""
    new_title = request.form["title"].strip()
    new_content = request.form["content"].strip()

    # post tags handling
    tids = [int(tid) for tid in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tids)).all()

    post = Post.query.get_or_404(post_id)

    if new_title:
        post.title = new_title
    if new_content:
        post.content = new_content
    post.tags = tags

    db.session.add(post)
    db.session.commit()
    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """delete post with id post_id"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{post.user_id}")
# --------------------------------------------------------------------------------

# Part 3 Routes ------------------------------------------------------------------

@app.route("/tags")
def all_tags():
    """Lists all tags, with links to the tag detail page."""
    tags = Tag.query.order_by(Tag.name.asc()).all()
    return render_template("tags.html", tags=tags)

@app.route("/tags/<int:tag_id>")
def tag_details(tag_id):
    """Show details about tag with id tag_id"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tagpage.html", tag=tag)

@app.route("/tags/new")
def tagform():
    """form page to create a new tag"""
    return render_template("tagform.html")

@app.route("/tags/new", methods=["POST"])
def tagform_submit():
    """create a new tag on submit of tag form"""
    tname = request.form["name"].strip()
    if len(tname) > 32 or not tname:
        flash("tag name must be between 1 and 32 characters", "danger")
        return redirect("/tags/new")
    tagnames = db.session.query(Tag).all()
    for tag in tagnames:
        if tname == tag.name:
            flash("Tag already exists", "warning")
            return redirect("/tags/new")
    newtag = Tag(name=tname)
    db.session.add(newtag)
    db.session.commit()
    return redirect("/tags")

@app.route("/tags/<int:tag_id>/edit")
def edit_tag(tag_id):
    """edit the tag with id tag_id"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tageditform.html", tag=tag)

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag_submit(tag_id):
    """edit the tag with id tag_id"""
    tag = Tag.query.get_or_404(tag_id)
    new_name = request.form["name"].strip()
    if len(new_name) > 32:
        flash("tag name must be between 1 and 32 characters", "danger")
        return redirect(f"/tags/{tag_id}/edit")
    if new_name:
        tagnames = db.session.query(Tag).all()
        for tag in tagnames:
            if new_name == tag.name:
                flash("Tag already exists", "warning")
                return redirect("/tags")
        tag.name = new_name
        db.session.add(tag)
        db.session.commit()
        return redirect("/tags")

@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """deletes the tag with id tag_id"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect("/tags")

# --------------------------------------------------------------------------------