from flask import Flask

app = Flask(__name__)


# http://localhost:5000
@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"
