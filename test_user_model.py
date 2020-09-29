"""User model tests, pattern matching from Warbler Springboard project."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Photos, Favorites

# different db for tests

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app
#
# in each test, we'll need to delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all() #create and drop db

        u1 = User.signup("HelloMello", "password") #use signup method to create a user instance
        uid1 = 1111 #designate the uid to make referencing it easier
        u1.id = uid1

        u2 = User.signup("GoodMorningStarshine", "password") #making another user copy
        uid2 = 2222
        u2.id = uid2

        db.session.commit() #committing the user copies to the session

        u1 = User.query.get(uid1) #establishing the variables
        u2 = User.query.get(uid2)

        self.u1 = u1 #storing all this info in self
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.client = app.test_client()

# Does User.signup successfully create a new user given valid credentials?
    def test_valid_signup(self):
        u_test = User.signup("test1", "password") #usimg signup method to create u to test against
        uid = 99999 #creating an id
        u_test.id = uid #assigning it to the u_test user
        db.session.commit() #committing to session

        u_test = User.query.get(uid) #fetching the test user from the session using uid
        self.assertIsNotNone(u_test) #testing that a value is there

        self.assertEqual(u_test.username, "test1") #testing that the username is the same as the test user's
        self.assertNotEqual(u_test.password, "password") #testing that the password is the same as the test user's
        # Bcrypt strings should start with $2b$
        self.assertTrue(u_test.password.startswith("$2b$")) #making sure the bcrypt strings are on the level

# Does User.signup fail to create a new user if the validations fail?
    def test_invalid_username_signup(self):
        invalid = User.signup(None, "password") #try to create user without username using signup method
        uid = 123456789 #creating id for invalid test user 
        invalid.id = uid #assigning the id to the invalid test user
        with self.assertRaises(exc.IntegrityError) as context: #use assertRaises to make sure the IntegrityError pops up
            db.session.commit() #commit to session
    
    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context: #make sure that when use signs up without entering pword a ValueError is raised
            User.signup("test2", "")

# Does User.authenticate successfully return a user when given a valid username and password?
    def test_valid_authentication(self):
        u = User.authenticate(self.u1.username, "password") #give a valid username/password
        self.assertIsNotNone(u) #check user existence
        self.assertEqual(u.id, self.uid1) #check u.id = u1 uid

# Does User.authenticate fail to return a user when the username is invalid?
    def test_invalid_username(self):
        self.assertFalse(User.authenticate("badusername", "password")) #check that a bad username is assertedFalse

# Does User.authenticate fail to return a user when the password is invalid?
    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.username, "badpassword")) #check that a bad pword is assertedFalse

#Does the basic model work?
    def test_user_model(self):

        u = User(
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no favorites yet
        self.assertEqual(len(u.favorites), 0)
    

    def tearDown(self):
        res = super().tearDown() #calling super on teardown allows us to test more than one heirarchy multiple times
        db.session.rollback() 
        return res