#from crypt import methods
import imp
from io import BytesIO
import os
from xml.dom.expatbuilder import DOCUMENT_NODE
from werkzeug.utils import secure_filename
from pickletools import read_uint1
from flask import (
    Flask,
    Blueprint,
    request,
    abort,
    flash,
    url_for,
    render_template,
    redirect,
    jsonify
)
from flask_login import login_required, current_user
from flaskr.models import *

main = Blueprint("main", __name__)

# Routes-----------------------------

@main.route("/home")
@login_required
def index():
    message = "Hello " + current_user.username + " !"
    fav_author = User.query.filter().all()
    return render_template("index.html", message=message, fav_author=fav_author)

@main.route("/users", methods=['GET'])
def view_users():
        try:
            users = User.query.all()

            if not users:
                abort(404)

            data = []
            for user in users:
                data.append(user.format())

            return jsonify({
                "success": True,
                "data": data
            })

        except Exception as e:
            err = e
            print("Err -> ", err)
            abort(404)

@main.route("/users/<int:user_id>", methods=['GET'])
def view_user(user_id):
        try:
            user = User.query.get(user_id)

            if not user:
                abort(404)            

            return jsonify({
                "success": True,
                "data": [{
                    "data" : user.format()
                }]
            })

        except Exception as e:
            err = e
            print("Err -> ", err)
            abort(404)


@main.route("/posts", methods=['GET', 'POST'])
def view_posts():
    if request.method == 'GET':
        try:
            posts = Post.query.all()

            if not posts:
                abort(404)

            data = []
            for post in posts:
                data.append({
                    'id': post.id,
                    'name': post.title
                })

            return jsonify({
                "success": True,
                "data": data
            })

        except Exception as e:
            err = e
            print("Err -> ", err)
            abort(404)
    else:
        pass

@main.route("/posts/<int:id>", methods=['GET'])
def view_post(post_id):
    try:
        post = Post.query.get(post_id)

        if not post:
            abort(404)

        return jsonify({
            "success": True,
            "data": [{
                "details" : post.format()
            }]
        })
    except Exception as e:
        err = e
        print("Err -> ", err)
        abort(404)


# Error handlers----------------------------

@main.errorhandler(400)
def bad_request(error):
    return render_template("error.html")


@main.errorhandler(404)
def not_found(error):
    return "There is no data to see here!"


@main.errorhandler(500)
def server_error(error):
    return render_template("error.html")
