"""Display Photos tests."""

# run these tests like:
#
# FLASK_ENV=production python -m unittest test_photos_views.py


from app import app, CURR_USER_KEY
import os
from unittest import TestCase

from models import db, connect_db, Photos, User, Favorites


#testing db below
os.environ['DATABASE_URL'] = "postgresql:///mars-test"

#creating tables
db.create_all()

# not testing wtf csrf

app.config['WTF_CSRF_ENABLED'] = False

class DisplayViewTestCase(TestCase):
    """Test views for users, pattern matching from warbler project"""

    def setUp(self):
        """creating test client and adding sample data"""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()  # creating test client

        self.testuser = User.signup(username="testuser",  # creating test user instance
                                    password="testuser",)

        self.testuser_id = 8989  # creating a user id
        self.testuser.id = self.testuser_id  # setting the user id to our test user

        db.session.commit()


    def test_show_photos(self):
        with app.test_client() as client:
            resp = client.get("/curiosity/photos") #attach route
            html = resp.get_data(as_text=True) #pull html resp
            self.assertIn("Mars", html) #test html
            self.assertIn("rover", html)
            self.assertEqual(resp.status_code, 200) #test that it shows

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp