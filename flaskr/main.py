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
)
from flask_login import login_required, current_user
from flaskr.models import *

main = Blueprint("main", __name__)

ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route("/home")
@login_required
def index():
    if current_user.is_admin:
        get_declarations = Declarations.query.all()
        declarations = [declaration.format() for declaration in get_declarations]

        return render_template("products.html", declarations=declarations)

    get_declarations = (
        Declarations.query.filter(Declarations.user_id == current_user.id)
        .order_by(Declarations.id.desc())
        .all()
    )
    declarations = [declaration.format() for declaration in get_declarations]

    return render_template("AddDeclaration.html", declarations=declarations)


@main.route("/add-declaration", methods=["GET", "POST"])
@login_required
def add_declarations():
    if request.method == "GET":
        return render_template("FilltheForm.html")
    else:
        nom_de_societe = request.form.get("nom_de_societe")
        ice = request.form.get("ice")
        rc = request.form.get("rc")
        identifiant = request.form.get("identifiant")
        nom_complet = request.form.get("nom_complet")
        cin = request.form.get("cin")
        capital = request.form.get("capital")
        date = request.form.get("date")
        statue = request.form.get("statue")
        centre_de_registre = request.form.get("centre_de_registre")
        numero = request.form.get("numero")
        type = request.form.get("type")
        document_id = None

        files = [request.files["file1"], request.files["file2"], request.files["file3"]]

        try:
            new_declaration = Declarations(
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
                current_user.id,
                type,
                number_of_documents=len(files),
            )
            new_declaration.insert()

            for file in files:
                if file.filename == "":
                    flash("No selected file")
                    abort(400)
                if file and allowed_file(file.filename):
                    document = Documents(
                        type=file.filename,
                        document=file.read(),
                        declaration=new_declaration.id,
                    )
                    document.insert()
        except:
            db.session.rollback()
            db.session.close()
            flash("Something went wrong")
            abort(500)
        return redirect(url_for("main.index"))


@main.route("/verify/<int:declaration_id>")
@login_required
def verify(declaration_id):
    get_declaration = Declarations.query.get(declaration_id)
    get_documents = (
        Documents.query.filter(Documents.declaration == declaration_id)
        .order_by(Documents.id.asc())
        .all()
    )

    documents = [document.id for document in get_documents]
    declaration = {"declaration": get_declaration, "documents": documents}

    return render_template("verification.html", declaration=declaration)


@main.route("/view/<int:document_id>")
@login_required
def show_file(document_id):
    document = Documents.query.get(document_id)
    return send_file(
        BytesIO(document.document),
        mimetype="application/pdf",
        attachment_filename=document.type,
    )


@main.route("/download/<int:document_id>")
@login_required
def download_file(document_id):
    document = Documents.query.get(document_id)
    return send_file(
        BytesIO(document.document),
        mimetype="application/pdf",
        attachment_filename=document.type,
        as_attachment=True,
    )


@main.route("/accept/<int:declaration_id>")
@login_required
def accept(declaration_id):
    declaration = Declarations.query.get(declaration_id)
    try:
        declaration.pending = False
        declaration.accepted = True
        declaration.update()
    except:
        abort(500)
    return redirect(url_for("main.index"))


@main.route("/reject/<int:declaration_id>")
@login_required
def reject(declaration_id):
    declaration = Declarations.query.get(declaration_id)
    try:
        declaration.pending = False
        declaration.accepted = False
        declaration.update()
    except:
        abort(500)
    return redirect(url_for("main.index"))


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
