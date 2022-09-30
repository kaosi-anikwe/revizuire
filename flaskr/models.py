from enum import unique
from multiprocessing.managers import SharedMemoryServer
import os
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Date, LargeBinary
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from dotenv import load_dotenv

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


class Users(UserMixin, db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(500), nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)

    def __init__(self, username, email, password):
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
        return {"id": self.id, "username": self.username, "email": self.email}


# Other tables------------

# Needs to be discussed
# What data exactly are we storing
# 
# posts - divided into paragraphs 
# likes
# shares 
# views
# comments
# ...etc 
# 
# I will prepare a table of what I think is neccessary and show you so you can approve