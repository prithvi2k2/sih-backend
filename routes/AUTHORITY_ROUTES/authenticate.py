# imports
from shutil import ExecError
import uuid
import os
import jwt
import hashlib
from functools import wraps
from routes.USER_ROUTES import client
from Logic_objects import location as loc
from datetime import datetime, timedelta
from flask import Blueprint, Flask, request, jsonify, make_response, current_app
from werkzeug.security import generate_password_hash, check_password_hash


authority = Blueprint('authority', __name__)


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


def Special_permissionAuth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        '''
        stuff here is validated and functions using this 
        decorater are not accessed bby anyone unless admin authority 
        basically to register all police ids
        '''
        return f(*args, **kwargs)
    return decorated


@authority.route("/AuthoritySignup",  methods=['POST'])
@API_required
def AuthoritySignup():
    try:
        data = dict(request.json)
        AuthorityID = data.get("AuthorityID", None)
        location = data.get("location", None)
        pw = data.get("pw", None)
        if not AuthorityID or not pw or not location:
            return make_response(jsonify(error="No Data payload!!")), 401

        location = loc.Location(location)
        if not location.__repr__():
            return make_response(jsonify(error="Cannot find the location specifies!!"))
        auth_obj = {
            "_id": str(uuid.uuid4()),
            "name": AuthorityID,
            "password": generate_password_hash(pw),
            "location": location.__repr__(),
            "case_ids": []
        }

        # connecting to mongo client
        db = client['crimes']
        collection = db["Authority_auth"]
        user_obj = collection.find_one({"name": AuthorityID})

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


@authority.route("/AuthorityLogin", methods=['POST'])
@API_required
def AuthorityLogin():
    try:
        data = dict(request.json)
        AuthorityID = data.get("AuthorityID", None)
        pw = data.get("pw", None)

        if not AuthorityID or not pw:
            return make_response(jsonify(error="No Data payload!!")), 401

        db = client['crimes']
        collection = db["Authority_auth"]
        user_obj = collection.find_one({"name": AuthorityID})

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
