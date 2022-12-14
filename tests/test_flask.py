from turtle import title
from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class BloglyUsersTestCase(TestCase):
    """Tests for Blogly Users app routes."""

    def setUp(self):
        """Deletes any existing users and puts in a test user."""
        User.query.delete()
        test_user = User(first_name="Testy",last_name="Testerson")
        db.session.add(test_user)
        db.session.commit()

        self.testuser = test_user

    def tearDown(self):
        """Rollback the session to clear it."""

        db.session.rollback()
    
    def test_users_page(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Blogly Users:</h1>', html)

    def test_user_info_page(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.testuser.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"<h1>{self.testuser.full_name}</h1>", html)
    
    def test_new_user(self):
        with app.test_client() as client:
            d = {"first_name":"secondary", "last_name":"testuser", "image_url" : ""}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("secondary testuser", html)
    
    def test_bad_new_user(self):
        with app.test_client() as client:
            d = {
                "first_name": "this first name is over thirty two characters",
                "last_name" : "this last name is over thirty two characters",
                "image_url" : ""
            }
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("First Name must be between 1 and 32 characters", html)
            self.assertIn("Last Name must be between 1 and 32 characters", html)

    def test_edit_user(self):
        with app.test_client() as client:
            d = {"first_name":"secondary", "last_name":"testuser", "image_url" : ""}
            resp = client.post(f"/users/{self.testuser.id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>secondary testuser</h1>", html)
    
    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.testuser.id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(self.testuser.full_name ,html)

class BloglyPostsTestCase(TestCase):
    """ Tests for app routes handling posts"""

    def setUp(self):
        """Deletes any existing users and posts and puts in a test user with a test post."""
        User.query.delete()
        test_user = User(first_name="Testy",last_name="Testerson")
        db.session.add(test_user)
        db.session.commit()

        Post.query.delete()
        test_post = Post(title="Test Post",
        content="This is the content of the test post", user_id=test_user.id)
        db.session.add(test_post)
        db.session.commit()

        self.testuser = test_user
        self.testpost = test_post

    def tearDown(self):
        """Rollback the session to clear it."""

        db.session.rollback()

    def test_post_page(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.testpost.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.testpost.readable_date,html)

    def test_new_post(self):
        with app.test_client() as client:
            d = {"title":"New Post", "content":"Unimportant"}
            resp = client.post(f"users/{self.testuser.id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("New Post" ,html)
    
    def test_post_delete(self):
        with app.test_client() as client:
            resp = client.post(f"/posts/{self.testpost.id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(self.testpost.title, html)
