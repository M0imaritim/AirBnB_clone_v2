#!/usr/bin/python3
"""module contains a minimalistic use of web framework flask"""


from flask import Flask
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_bnb():
    """directing to home directory/page"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """directing to another page"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_route(text):
    """directing to another page"""
    text = text.replace('_', ' ')
    return "C {}".format(text)


@app.route("/python/", defaults={'text': 'is_cool'}, strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def py_route(text):
    """directing to another page"""
    text = text.replace('_', ' ')
    return "Python {}".format(text)


@app.route("/number/<int:n>", strict_slashes=False)
def number(n):
    """directing to another page"""
    return "{} is a number".format(n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
