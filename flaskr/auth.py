from flask import Blueprint, flash, request, redirect, url_for, render_template
from flaskr.models import db, Users
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)


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
        email = request.form.get("email")
        username = request.form.get("username")

        user = Users.query.filter(Users.username == username, Users.email == email).first()
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
