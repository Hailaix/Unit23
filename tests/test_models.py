from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests for model for Users."""

    def setUp(self):
        """Deletes any existing Users."""
        User.query.delete()

    def tearDown(self):
        """Rollback the session to clear it."""

        db.session.rollback()


    def test_full_name(self):
        user = User(first_name="Testy",last_name="Testerson")
        self.assertEquals(user.full_name, "Testy Testerson")
