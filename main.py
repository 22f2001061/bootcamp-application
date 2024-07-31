from flask import Flask, request, render_template, url_for, redirect, flash, session
from app.models import User, Section
from app.config import LocalConfig
from app.db import db
from werkzeug.security import generate_password_hash

import os
from werkzeug.utils import secure_filename

from app.bp.auth import bp as auth_bp
from app.bp.section import bp as section_bp
from app.bp.book import bp as book_bp
from app.bp.book_issue import bp as book_issue_bp

from app.api.section import ListSectionResource, SectionResource


app = Flask(__name__)
app.config.from_object(LocalConfig)
db.init_app(app)


# http://localhost:5000/
@app.route("/")
def homepage():
    userdetails = {
        "user_id": session.get("user_id"),
        "username": session.get("username"),
        "role": session.get("role"),
    }
    return render_template("homepage.html", user=userdetails)


@app.route("/create-tables")
def create_tables():
    try:
        with app.app_context():
            db.create_all()
    except Exception as e:
        raise e
        return f"Something Went wrong {str(e)}"
    return "TABLES CREATED SUCCESFULLY"


app.register_blueprint(auth_bp)
app.register_blueprint(section_bp)
app.register_blueprint(book_bp)
app.register_blueprint(book_issue_bp)

from flask_restful import Resource, Api

api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {"hello": "world"}

    def post(self):
        return {"post": "request"}

    def put(self):
        pass

    def delete(self):
        pass


api.add_resource(HelloWorld, "/api/v1/")
api.add_resource(ListSectionResource, "/api/v1/sections")
api.add_resource(SectionResource, "/api/v1/sections/<id>")


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


@app.route("/upload-file-demo", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash("No selected file", "warning")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print(file.filename)
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return redirect(url_for("download_file", name=filename))
    return render_template("file_upload.html")


@app.route("/download-file")
def download_file():
    name = request.args.get("name")
    return render_template("download_file.html", filename=name)


if __name__ == "__main__":
    app.run()
