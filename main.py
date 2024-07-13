from flask import Flask

app = Flask(__name__)


# http://localhost:5000/
@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"


@app.route("/hello")
def hello():
    return "<h1>Hello, World!</h1>"


if __name__ == "__main__":
    app.run(debug=True)
