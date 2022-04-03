from flask import Blueprint
from database import mongo

user = Blueprint('user', __name__)


@user.route("/signup")
def signup():
    return "Signup page"


@user.route("/login")
def login():
    return "Login page"

# Hash usernames with hashlib
# salt hash passwords with bcrypt

# salt = bcrypt.gensalt()
# username = bcrypt.hashpw('prithvi2k2'.encode('utf8'), salt)
# password = bcrypt.hashpw('test@12321'.encode('utf8'), salt)
# print(username, password)
# bcrypt doesnt have plain hashing
# print(hash('prithvi2k2'))

# if bcrypt.checkpw('prithvi2k2'.encode('utf8'), b'$2b$12$o9ZGHp05ZdLaNNc665.G0usE7HeZBIZQ9QDgNRuEjsigYBzWsLqm6'):
#     print("match")
# else:
#     print("does not match")