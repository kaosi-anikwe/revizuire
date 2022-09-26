from enum import unique
import os
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Date, LargeBinary
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy
from flask import send_file
from flask_login import UserMixin
from dotenv import load_dotenv

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
    db.init_app(app)
    db.create_all()

    """
    Models
    """


class Users(UserMixin, db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(50), nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    declarations = relationship(
        "Declarations", cascade="all, delete-orphan", backref=backref("user")
    )

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {"id": self.id, "username": self.username, "email": self.email}


class Declarations(db.Model):
    __tablename__ = "declaration"

    id = Column(Integer, primary_key=True)
    nom_de_societe = Column(String(20))
    ice = Column(String(20))
    rc = Column(String(100))
    identifiant = Column(String(20))
    nom_complet = Column(String(100))
    cin = Column(String(100))
    capital = Column(String(50))
    date = Column(Date)
    statue = Column(String(50))
    centre_de_registre = Column(String(50))
    numero = Column(String(20))
    pending = Column(Boolean, nullable=False, default=True)
    accepted = Column(Boolean, nullable=False, default=False)
    type = Column(String(100), nullable=False)
    number_of_documents = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))

    def __init__(
        self,
        nom_de_societe,
        ice,
        rc,
        identifiant,
        nom_complet,
        cin,
        capital,
        date,
        statue,
        centre_de_registre,
        numero,
        user_id,
        type,
        number_of_documents,
    ):
        self.nom_de_societe = (nom_de_societe,)
        self.ice = (ice,)
        self.rc = (rc,)
        self.identifiant = (identifiant,)
        self.nom_complet = (nom_complet,)
        self.cin = (cin,)
        self.capital = (capital,)
        self.date = (date,)
        self.statue = (statue,)
        self.centre_de_registre = (centre_de_registre,)
        self.numero = (numero,)
        self.user_id = (user_id,)
        self.type = type
        self.number_of_documents = number_of_documents

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "nom_de_societe": self.nom_de_societe,
            "ice": self.ice,
            "rc": self.rc,
            "identifiant": self.identifiant,
            "nom_complet": self.nom_complet,
            "cin": self.cin,
            "capital": self.capital,
            "date": self.date,
            "statue": self.statue,
            "centre_de_registre": self.centre_de_registre,
            "numero": self.numero,
            "pending": self.pending,
            "accepted": self.accepted,
            "user_id": self.user_id,
            "type": self.type,
            "number_of_documents": self.number_of_documents,
        }


class Documents(db.Model):
    __tablename__ = "document"

    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False)
    document = Column(LargeBinary(length=(2**32) - 1), nullable=False)
    declaration = Column(Integer, ForeignKey("declaration.id"))

    def __init__(self, type, document, declaration):
        self.type = type
        self.document = document
        self.declaration = declaration

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "type": self.type,
            "document": self.document,
            "declaration": self.declaration,
        }
