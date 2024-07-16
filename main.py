from flask import Flask, request, render_template, url_for, redirect, flash
from models import User
from config import LocalConfig
from db import db
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config.from_object(LocalConfig)
db.init_app(app)


# http://localhost:5000/
@app.route("/")
def homepage():
    return render_template("homepage.html")


@app.route("/register", methods=["GET", "POST"])
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
            return redirect(url_for("register"))
        # make an entry into users table to create a new user
        if pass_hash:
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

        # return the response or redirect to login
        return redirect(url_for("homepage"))


@app.route("/create-tables")
def create_tables():
    try:
        with app.app_context():
            db.create_all()
    except Exception as e:
        return f"Something Went wrong {str(e)}"
    return "TABLES CREATED SUCCESFULLY"


if __name__ == "__main__":
    app.run()
