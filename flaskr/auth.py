from flask import Blueprint, flash, request, redirect, url_for, render_template
from flaskr.models import db, Users
from flask_login import login_user, login_required, logout_user, current_user
import hashlib

auth = Blueprint("auth", __name__)

def getHashed(text):  # function to get hashed email/password as it is reapeatedly used
    salt = "ITSASECRET"  # salt for password security
    hashed = text + salt  # salt for password security, a random string will be added to password and hashed together below
    hashed = hashlib.md5(hashed.encode())  # encrypting with md5 hash, best for generating passwords for db
    hashed = hashed.hexdigest()  # converting to string
    return hashed  # gives hashed text back

@auth.route("/")
def landing():
    return redirect(url_for("auth.login"))


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if not current_user.is_active:
            return render_template("login.html")
        return redirect(url_for("main.index"))

    else:
        email = request.form.get("username")
        username = request.form.get("password")

        user = Users.query.filter(Users.username == username, Users.password == getHashed(email)).first()
        if user:
            login_user(user)
            return redirect(url_for("main.index"))
        else:
            flash("Incorrect email")
            return render_template("login.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
