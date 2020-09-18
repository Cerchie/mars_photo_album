"""SQLAlchemy models."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connecting the db. (Call in app.py)
    """

    db.app = app
    db.init_app(app)


class User(db.Model):
    """makes user table  with id, username, and password columns"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    username = db.Column(
        db.String(30),
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    favorites = db.relationship(
        'Photos',
        secondary="favorites"
    )

    def __repr__(self):
        return f"<User #{self.id}: {self.username}>"

    @classmethod
    def signup(cls, username, password):

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Favorites(db.Model):
"""makes favorites table with id, user_id, and photo_id columns"""
    __tablename__ = 'favorites'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    photo_id = db.Column(
        db.Integer,
        db.ForeignKey('photos.id', ondelete='cascade')
    )

class Photos(db.Model):
"""makes photos table with id and url columns"""
    __tablename__ = 'photos'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    image_url = db.Column(
        db.Text,
        nullable=False,
    )