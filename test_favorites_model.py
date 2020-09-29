
"""Faves model tests."""

# run these tests like:
#
#    python -m unittest test_favorites_model.py


from app import app
import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Photos, Favorites

os.environ['DATABASE_URL'] = "postgresql:///mars-test"


# Now we can import app

from app import app

db.create_all()


class FavoritesModelTestCase(TestCase):
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

        p = Photos(  # creating sample photo
           id= 2222, image_url="https://images.unsplash.com/photo-1500375592092-40eb2168fd21?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80"
        )
        db.session.add(p)
        db.session.commit()  # adding to sesh
        f = Favorites(  # creating photo
            photo_id = p.id, user_id = self.u.id
        )

        db.session.add(f)
        db.session.commit()  # adding to sesh
   
        # check that there is one photo present in favorites
        self.assertEqual(len(self.u.favorites), 1)

    def tearDown(self):
        # calling super on teardown allows us to test more than one heirarchy multiple times
        res = super().tearDown()
        db.session.rollback()
        return res