from flask import Blueprint, redirect, request, url_for, render_template, session, flash
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

from app.db import db
from app.models import User


bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        # get the form data from request
        first_name = request.form.get("fname")
        lname = request.form.get("lname")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmPassword = request.form.get("cofirmPassword")
        if password == confirmPassword:
            pass_hash = generate_password_hash(password)
        else:
            flash("Confirm password should be same as Passord", "warning")
            return redirect(url_for("auth.register"))
        # make an entry into users table to create a new user
        if pass_hash:
            try:
                new_user = User(
                    fname=first_name,
                    lname=lname,
                    username=username,
                    email=email,
                    role="student",
                    password=pass_hash,
                )
                db.session.add(new_user)
                db.session.commit()
            except IntegrityError as e:
                flash("User with username or email already exist", "info")
                return redirect(url_for("auth.register"))

        # return the response or redirect to login
        return redirect(url_for("auth.login"))


def authenticate(user_password, password):
    return user_password == password


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter(username == username).first()
        is_authenticated = authenticate(user.password, password)
        if is_authenticated:
            session["username"] = user.username
            session["role"] = user.role
            return redirect(url_for("homepage"))
        else:
            flash("Credintials do not match", "warning")
            return redirect(url_for("auth.login"))


@bp.route("/logout", methods=["GET", "POST"])
def logout():
    if request.method == "GET":
        return render_template("logout.html")
    elif request.method == "POST":
        try:
            session.pop("username")
            session.pop("role")
        except:
            pass
        return redirect(url_for("homepage"))
