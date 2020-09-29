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
# LOGIN/LOGOUT ROUTES
#___________________________________

    def test_login(self):
        with app.test_client() as client:
            resp = client.get(f"/login") #attach route
            html = resp.get_data(as_text=True) #pull html resp
            self.assertIn("return home", html)
            self.assertEqual(resp.status_code, 200) #check that route comes back
    def test_logout(self):
        with app.test_client() as client:
            resp = client.get(f"/logout") #attach route
            self.assertEqual(resp.status_code, 302) #check that route redirects
#___________________________________
# USER CAPABILITIES
#___________________________________

    def test_show_editpage(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.testuser_id}/edit") #attach route
            html = resp.get_data(as_text=True) #pull html resp
            self.assertIn("<title>", html) #test redirecting html
            self.assertEqual(resp.status_code, 302) #test that it redirects

    def test_edit_user(self):
        with app.test_client() as client:
            d = {"username": "Chickens2", "password": "Scratchscratch"} #set up JSON
            resp = client.post(f"/users/{self.testuser_id}/edit", data=d, follow_redirects=True)  #post JSON to route
            self.assertEqual(resp.status_code, 200) #check that route comes back

    def test_show_user_page(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.testuser_id}/edit") #attach route
            html = resp.get_data(as_text=True) #pull html resp
            self.assertIn("Redirecting", html) #testing html resp
            self.assertEqual(resp.status_code, 302) #check that route redirects


#___________________________________
# CREATE/DELETE USER ROUTES
#___________________________________
    def test_add_user(self):
        with app.test_client() as client:
            d = {"username": "Lucy2", "password": "Narnia"} #set up JSON
            resp = client.post("/users/signup", data=d, follow_redirects=True) #post JSON to route
            self.assertEqual(resp.status_code, 200) #check that route comes back
    
    def test_delete(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.testuser_id}/delete")
            html = resp.get_data(as_text=True)
            self.assertNotIn("Please login.", html) #test that user is logged in
            self.assertNotIn(f"{self.testuser_id}", str(resp.data)) #test that username is not in resp
            self.assertEqual(resp.status_code, 302) #test that route redirects properly
#___________________________________
# when you’re logged out, are you disallowed from visiting unauthorized pages?
#___________________________________
    def test_unauthorized_users_favorites(self):
        with self.client as c:
            resp = c.get(f"/users/{self.testuser_id}/favorites", follow_redirects = True) #grabbing route
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
            resp = c.get(f"users/{self.testuser_id}/delete", follow_redirects = True) #grabbing route
            self.assertEqual(resp.status_code, 200)  # route shows up
            self.assertNotIn("@abc", str(resp.data))
            # and that the error msg shows
            self.assertIn("Please login.", str(resp.data))

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp