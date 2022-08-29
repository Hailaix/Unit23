from unittest import TestCase

from app import app
from models import db, User

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