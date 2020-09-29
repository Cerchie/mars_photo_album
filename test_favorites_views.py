"""Favorites View tests."""

# run these tests like:
#
# FLASK_ENV=production python -m unittest test_favorites_views.py


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

    def setup_faves(self):  # setting up faves for faves tests
        # creating 3 photos, last is the only one with id
        p1 = Photos(image_url="https://images.unsplash.com/photo-1464802686167-b939a6910659?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2533&q=80",)
        p2 = Photos(image_url="https://images.unsplash.com/photo-1601132359864-c974e79890ac?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1502&q=80",)
        p3 = Photos(id=9876, image_url="https://images.unsplash.com/photo-1484662020986-75935d2ebc66?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1500&q=80",)
        db.session.add_all([p1, p2, p3])
        db.session.commit()  # adding and committing to session

        f1 = Favorites(user_id=self.testuser_id,
                   photo_id=9876)  # setting up faves

        db.session.add(f1)
        db.session.commit()  # committing faves to session

    def test_add_fave(self):
        # creating photo instance and adding to session
        p = Photos(id=1984,
                    image_url="https://images.unsplash.com/photo-1464802686167-b939a6910659?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2533&q=80")  # creating a favorite instance
        db.session.add(p)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                # checking that user must be signed in
                sess[CURR_USER_KEY] = self.testuser_id
            # setting route to fave instance
            resp = c.post("/photos/1984/favorite", follow_redirects=True)
            # checking that page shows up
            self.assertEqual(resp.status_code, 200)
            # getting faves with photo_id 1984
            faves = Favorites.query.filter(Favorites.photo_id == 1984).all()
            # checking that the number of faves = 1
            self.assertEqual(len(faves), 1)
            # checking that the faves with the user_id we have matches our test fave
            self.assertEqual(faves[0].user_id, self.testuser_id)

    def test_remove_fave(self):
        self.setup_faves()  # setting up faves

        p = Photos.query.filter(
            Photos.id == 9876)  # finding photo
        self.assertIsNotNone(p)  # checking that it's not None
    

        f = Favorites.query.filter(
            Favorites.user_id == self.testuser_id and Favorites.user_id == p.id
        ) # checking to see that this fave is an intersection of p id and user id

        # Now we are sure that testuser faves the photo
        self.assertIsNotNone(f)  # checking that the value of fave is not None

        with self.client as c:
            with c.session_transaction() as sess:
                # checking that user is logged in
                sess[CURR_USER_KEY] = self.testuser.id

            # setting up the response as /photos/id/favorite, this route will delete if favorite in the system
            resp = c.post(f"/photos/9876/favorite", follow_redirects=True)
            # checking that we get the response
            self.assertEqual(resp.status_code, 200)

            # setting up favorites as the faves with p_id = to id of fave
            favorites = Favorites.query.filter(Favorites.photo_id == 1984).all()
    
            #  #checking that the length of these likes is 0
            self.assertEqual(len(favorites), 0)






    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp