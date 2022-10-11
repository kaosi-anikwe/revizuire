from enum import unique
from multiprocessing.managers import SharedMemoryServer
import os
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Date, LargeBinary
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from dotenv import load_dotenv
from flask_migrate import Migrate

# get credentials from .env file
load_dotenv()

database_name = os.getenv("DATABASE_NAME")
database_username = os.getenv("DATABASE_USERNAME")
database_password = os.getenv("DATABASE_PASSWORD")
host = os.getenv("HOST")
database_path = "mysql://{}:{}@{}/{}".format(
    database_username, database_password, host, database_name
)

db = SQLAlchemy()

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
    db.create_all()

    """
    Models
    """


class Users(UserMixin, db.Model):
    __tablename__ = "user"

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
        return {"id": self.id, "first_name": self.first_name, "last_name": self.last_name, "username": self.username, "email": self.email}

# My apologies guys, this is what I have so far