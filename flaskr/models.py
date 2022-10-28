from datetime import date
from enum import unique
from multiprocessing.managers import SharedMemoryServer
import os
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Boolean, Date, LargeBinary
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from dotenv import load_dotenv
from flask_migrate import Migrate

from flask_migrate import Migrate


db = SQLAlchemy()

# get credentials from .env file
load_dotenv()

database_name = os.getenv("DATABASE_NAME")
database_username = os.getenv("DATABASE_USERNAME")
database_password = os.getenv("DATABASE_PASSWORD")
host = os.getenv("HOST")
database_path = "mysql://{}:{}@{}/{}".format(
    database_username, database_password, host, database_name
)


"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    migrate = Migrate(app, db)
    db.init_app(app)
    migrate.init_app(app, db)
    # db.create_all()

    """
    Models
    """


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(500), nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    number_of_posts = Column(Integer)
    number_of_likes = Column(Integer)
    number_of_dislikes = Column(Integer)
    posts = relationship('Post', secondary='posts', backref=db.backref(
        'users', lazy=True
    ))

    def __init__(self, first_name, last_name, username, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email
        }


class Post(db.Model):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    text = Column(String(2048))
    user_id = Column(ForeignKey('users.id'), nullable=False)
    datetime = Column(DateTime(timezone=True), server_default=func.now())
    number_of_likes = Column(Integer)
    number_of_comments = Column(Integer)
    number_of_views = Column(Integer)
    number_of_clicks = Column(Integer)
    category = Column(String(50))

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "Title": self.title,
            "Text": self.text,
            "Author": self.user_id
        }


class View(db.Model):
    __tablename__ = "views"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)


class Click(db.Model):
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)


class Like(db.Model):
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)


class Comment(db.Model):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    text = Column(String(250), nullable=False)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    is_reply = Column(Boolean)
    comment_id = Column(Integer)
    datetime = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, text, user_id):
        self.text = text
        self.user_id = user_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "Comment": self.text,
            "Author": self.user_id
        }
