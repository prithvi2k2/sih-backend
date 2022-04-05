# imports
from shutil import ExecError
import uuid
import os
import jwt
import hashlib
from functools import wraps
from database import mongo
from routes.USER_ROUTES import client

from datetime import datetime, timedelta
from flask import Blueprint, Flask, request, jsonify, make_response, current_app
from werkzeug.security import generate_password_hash, check_password_hash


user = Blueprint('user', __name__)


# inits
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None
        print("my boii")

        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return make_response(jsonify({'message': 'Token is missing !!'})), 401

        # jwt validation
        try:
            data = jwt.decode(
                token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            db = client['crimes']
            collection = db["crimes_auth"]
            current_user = collection.find_one({"_id": data["public_id"]})
        except Exception as e:
            print(e,  e.__traceback__.tb_lineno)
            return make_response(jsonify({
                'message': 'unable to find user'
            })), 401

        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)
    return decorated


def API_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # jwt is passed in the request header
        if 'X-API-Key' in request.headers:
            api_key = request.headers['X-API-Key']
        if not api_key:
            return make_response(jsonify({'message': 'APIKEY is missing !!'})), 511
        if str(api_key) == str(os.getenv('API_KEY')):
            # print("thank god")
            pass
        else:
            return make_response(jsonify({
                'message': 'api_key is invalid !!'
            })), 401

        # returns the current logged in users contex to the routes
        return f(*args, **kwargs)
    return decorated


@user.route("/signup",  methods=['POST'])
@API_required
def signup():
    try:
        data = dict(request.json)
        wallet_addr, user = data.get(
            "wallet_addr", None), data.get("user", None)
        pw = data.get("pw", None)
        if not user or not pw:
            return make_response(jsonify(error="No Data payload!!")), 401

        hash_user = hashlib.sha256(user.encode('utf-8'))
        user_hex = hash_user.hexdigest()
        print(user_hex)
        auth_obj = {
            "_id": str(uuid.uuid4()),
            "name": user_hex,
            "wallet_addr": wallet_addr if wallet_addr else None,
            "password": generate_password_hash(pw),
            "case_ids": []
        }

        # connecting to mongo client
        db = client['crimes']
        collection = db["crimes_auth"]
        user_obj = collection.find_one({"name": user_hex})

        if user_obj != None:
            return make_response(jsonify(user_exits=True, token=None)), 401

        collection.insert_one(auth_obj)
        # jwt generation
        token = jwt.encode({
            'public_id': auth_obj["_id"],
            'exp': datetime.utcnow() + timedelta(weeks=2)
        }, current_app.config['SECRET_KEY'])
        return make_response(jsonify(user_exits=False, token=token), 201)
    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(error=e)), 401


@user.route("/login", methods=['POST'])
@API_required
def login():
    try:
        data = dict(request.json)
        user = data.get("user", None)
        pw = data.get("pw", None)

        if not user or not pw:
            return make_response(jsonify(error="No Data payload!!")), 401

        hash_user = hashlib.sha256(user.encode('utf-8'))
        user_hex = hash_user.hexdigest()
        print(user_hex)
        db = client['crimes']
        collection = db["crimes_auth"]
        user_obj = collection.find_one({"name": user_hex})

        if user_obj == None:
            print("lmaoooee")
            return make_response(jsonify(user_exits=False, login=False, token=None)), 401

        if not check_password_hash(user_obj["password"], pw):
            print("loll")
            return make_response(jsonify(login=False, user_exits=True,  token=None), 201)

        token = jwt.encode({
            'public_id': user_obj["_id"],
            'exp': datetime.utcnow() + timedelta(weeks=2)
        }, current_app.config['SECRET_KEY'])
        return make_response(jsonify(login=True, user_exits=True,  token=token), 201)
    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(error=e)), 401


@user.route('/change_wallet', methods=['POST'])
@API_required
@token_required
def change_wallet(current_user):
    try:
        data = dict(request.json)
        new_addr = data.get("new_addr", None)
        current_user["wallet_addr"] = new_addr
        del current_user["password"]

        db = client['crimes']
        collection = db["crimes_auth"]

        collection.update_one({"_id": current_user["_id"]}, {
                              "$set": {"wallet_addr": current_user["wallet_addr"]}})
        return jsonify(current_user)
    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(error=e)), 401


# default route to authenticate or for init
@user.route('/test')
@API_required
@token_required
def test(current_user):
    print(current_user)
    return "reyy"


@user.route('/Get_UserCases',  methods=['GET'])
@API_required
@token_required
def Get_UserCases(current_user):
    return make_response(jsonify(cases=current_user["case_ids"]))

# ---------------------------------------------------------------------------------
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
