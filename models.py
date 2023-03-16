"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()


def connect_db(app):
    """connect to database"""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Database models and methods for Users"""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    first_name = db.Column(
        db.String(30),
        nullable=False
    )

    last_name = db.Column(
        db.String(30),
        nullable=False
    )

    image_url = db.Column(
        db.Text,
        nullable=False
    )

    @classmethod
    def add_user(cls, user):
        """Adds user to database"""
        db.session.add(user)
        db.session.commit()

    @classmethod
    def edit_user(cls, user, first, last, img):
        """Takes user data and updates data in database"""

        user.first_name = first
        user.last_name = last
        user.image_url = img
        db.session.commit()

    @classmethod
    def delete_user(cls, user):
        """Given a user, delete it from the database"""

        db.session.delete(user)
        db.session.commit()


class Post(db.Model):
    """Model for user posts"""

    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    title = db.Column(
        db.String(50),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now()
    )
