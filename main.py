from flask import Flask, request, render_template, url_for

app = Flask(__name__)


# http://localhost:5000/
@app.route("/")
def homepage():
    return render_template("homepage.html")


@app.route("/hello")
def hello():
    return render_template("hello.html")


if __name__ == "__main__":
    app.run(debug=True)
