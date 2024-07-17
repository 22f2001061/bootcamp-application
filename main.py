from flask import Flask, request, render_template, url_for, redirect, flash, session
from app.models import User, Section
from app.config import LocalConfig
from app.db import db
from werkzeug.security import generate_password_hash

from app.bp.auth import bp as auth_bp


app = Flask(__name__)
app.config.from_object(LocalConfig)
db.init_app(app)


# http://localhost:5000/
@app.route("/")
def homepage():
    userdetails = {"username": session.get("username"), "role": session.get("role")}
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


if __name__ == "__main__":
    app.run()
