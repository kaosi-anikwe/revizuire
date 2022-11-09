from crypt import methods
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
    return render_template("index.html", message=message)




# Error handlers----------------------------

@main.errorhandler(400)
def bad_request(error):
    return render_template("error.html")


@main.errorhandler(404)
def not_found(error):
    return render_template("error.html")


@main.errorhandler(500)
def server_error(error):
    return render_template("error.html")
