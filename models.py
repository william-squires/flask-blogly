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

    posts = db.relationship("Post", backref="user")

    @classmethod
    def add_user(cls, user):
        """Adds user to database"""
        db.session.add(user)
        db.session.commit()

    def edit_user(self, first, last, img):
        """Takes user data and updates data in database"""

        self.first_name = first
        self.last_name = last
        self.image_url = img
        


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
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    @classmethod
    def add_new_post(cls, post):
        """Adds new post to user profile"""

        db.session.add(post)
        db.session.commit()

    def edit_post(self, title, content):
        """Edits post information"""       
        
        self.title = title
        self.content = content

        db.session.commit()
