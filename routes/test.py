from flask import Blueprint

test = Blueprint('test', __name__)

@test.route("/")
def live():
    return "Up and running!"