
"""Photos model tests."""

# run these tests like:
#
#    python -m unittest test_photos_model.py


from app import app
import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Photos, Favorites

os.environ['DATABASE_URL'] = "postgresql:///mars-test"


# Now we can import app

from app import app

db.create_all()


class PhotoModelTestCase(TestCase):
    """Test views for photos."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.uid = 94566
        u = User.signup("testing", "password")
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()


# Does the model work on a basic level?
    def test_photo_model(self):
        """Does basic model work?"""

        p = Photos(  # creating photo
            image_url="https://images.unsplash.com/photo-1500375592092-40eb2168fd21?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80"
        )
        self.u.favorites.append(p)
        db.session.add(p)
        db.session.commit()  # adding to sesh
   
        # check that there is one photo present in favorites
        self.assertEqual(len(self.u.favorites), 1)

# Does the model successfully detect when user2 faves photo1?
# Does the model successfully detect when photo1 belongs to the faves of user2?

    def test_photo_faves(self):
        p1 = Photos(  # creating photo
            image_url="https://images.unsplash.com/photo-1500375592092-40eb2168fd21?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80"
        )

        p2 = Photos(  # creating photo
            image_url="https://images.unsplash.com/photo-1444944232907-0b9e9ace348c?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=80"
        )

        # creating a test user instance
        u = User.signup("testing12", "password")
        uid = 888  # creating an id
        u.id = uid  # assigning it to our test user
        db.session.add_all([p1, p2, u])  # adding to sesh
        db.session.commit()  # committing

        u.favorites.append(p1)  # adding p1 to user faves

        db.session.commit()  # committing

        # find faves where their user id = the test user id
        f = Favorites.query.filter(Favorites.user_id == uid).all()
        self.assertEqual(len(f), 1)  # there should be one
        # the id of the first photo in the fave

    def tearDown(self):
        # calling super on teardown allows us to test more than one heirarchy multiple times
        res = super().tearDown()
        db.session.rollback()
        return res