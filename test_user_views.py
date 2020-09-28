"""User View tests."""

# run these tests like:
#
# FLASK_ENV=production python -m unittest test_user_views.py


from app import app, CURR_USER_KEY
import os
from unittest import TestCase

from models import db, connect_db, Photos, User, Favorites
from bs4 import BeautifulSoup

#testing db below
os.environ['DATABASE_URL'] = "postgresql:///mars-test"

#creating tables
db.create_all()

# not testing wtf csrf

app.config['WTF_CSRF_ENABLED'] = False

class UserViewTestCase(TestCase):
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

        self.u1 = User.signup("abc",
                              "password")  # creating test user 1
        self.u1_id = 778  # creating a user id
        self.u1.id = self.u1_id  # setting the user id to our test user
        self.u2 = User.signup("efg",
                              "password")  # creating test user 2
        self.u2_id = 884  # creating a user id
        self.u2.id = self.u2_id  # setting the user id to our test user
        # creating test user 3, no id
        self.u3 = User.signup("hij", "password")
        # creating test user 4, no id
        self.u4 = User.signup("testing", "password")

        db.session.commit()



    def test_user_edit_page(self): 
        with self.client as c:
            resp = c.get(f"/users/{self.testuser_id}/edit")  # route is users/userid

            self.assertEqual(resp.status_code, 302)  # redirect happens when user is not signed in
#___________________________________
# When you’re logged out, are you disallowed from visiting unauthorized pages?
#___________________________________
    def test_unauthorized_users_favorites(self):
        with self.client as c:
            resp = c.get(f"/{self.testuser_id}/favorites", follow_redirects = True) #grabbing route
            self.assertEqual(resp.status_code, 200)  # route shows up
            self.assertNotIn("@abc", str(resp.data))
            # and that the error msg shows
            self.assertIn("Please login.", str(resp.data))

    def test_unauthorized_users_homepage(self):
        with self.client as c:
            resp = c.get(f"/{self.testuser_id}/homepage", follow_redirects = True) #grabbing route
            self.assertEqual(resp.status_code, 200)  # route shows up
            self.assertNotIn("@abc", str(resp.data))
            # and that the error msg shows
            self.assertIn("Please login.", str(resp.data))

    def test_unauthorized_users_edit_page(self):
        with self.client as c:
            resp = c.get(f"/users/{self.testuser_id}/edit", follow_redirects = True) #grabbing route
            self.assertEqual(resp.status_code, 200)  # route shows up
            self.assertNotIn("@abc", str(resp.data))
            # and that the error msg shows
            self.assertIn("Please login.", str(resp.data))

    def test_unauthorized_users_delete(self):
        with self.client as c:
            resp = c.get(f"/{self.testuser_id}/delete", follow_redirects = True) #grabbing route
            self.assertEqual(resp.status_code, 200)  # route shows up
            self.assertNotIn("@abc", str(resp.data))
            # and that the error msg shows
            self.assertIn("Please login.", str(resp.data))

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp