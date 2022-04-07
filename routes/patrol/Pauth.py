import uuid
from argon2 import PasswordHasher
import jwt
from functools import wraps
from config import db
import config
from Logic_objects import location as loc
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, make_response


patrol = Blueprint('patrol', __name__)


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
                token, config.SECRET_KEY, algorithms=["HS256"])
            current_user = db.patrol.find_one({"_id": data["public_id"]})
        except Exception as e:
            print(e,  e.__traceback__.tb_lineno)
            return make_response(jsonify({
                'message': 'unable to find patrol authority'
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
        if str(api_key) == config.API_KEY:
            # print("thank god")
            pass
        else:
            return make_response(jsonify({
                'message': 'api_key is invalid !!'
            })), 401

        # returns the current logged in users context to the routes
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


@patrol.route("/signup",  methods=['POST'])
@API_required
def signup():
    try:
        req = dict(request.json)
        AuthorityID = req.get("AuthorityID")
        location = req.get("location")
        pw = req.get("password")
        if not AuthorityID or not pw or not location:
            return make_response(jsonify(error="No Data payload!!"), 401)

        location = loc.Location(location)
        if not location.__repr__():
            return make_response(jsonify(error="Cannot find the location specifies!!"))
        auth_obj = {
            "_id": str(uuid.uuid4()),
            "name": AuthorityID,
            "password": Phash(pw),
            "location": location.__repr__(),
            "case_ids": []
        }

        user_obj = db.patrol.find_one({"name": AuthorityID})

        if user_obj != None:
            return make_response(jsonify(user_exists=True, token=None), 401)

        db.patrol.insert_one(auth_obj)
        # jwt generation
        token = jwt.encode({
            'public_id': auth_obj["_id"],
            'exp': datetime.utcnow() + timedelta(weeks=2)
        }, config.SECRET_KEY)
        return make_response(jsonify(user_exists=False, token=token), 201)
    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(error=e), 401)


@patrol.route("/login", methods=['POST'])
@API_required
def login():
    try:
        req = dict(request.json)
        AuthorityID = req.get("AuthorityID")
        pw = req.get("password")

        if not AuthorityID or not pw:
            return make_response(jsonify(error="No Data payload!!"), 401)

        user_obj = db.patrol.find_one({"name": AuthorityID})

        if user_obj == None:
            print("lmaoooee")
            return make_response(jsonify(user_exists=False, login=False, token=None), 401)

        if not verifyPass(user_obj["password"], pw):
            print("loll")
            return make_response(jsonify(login=False, user_exists=True,  token=None), 201)

        token = jwt.encode({
            'public_id': user_obj["_id"],
            'exp': datetime.utcnow() + timedelta(weeks=2)
        }, config.SECRET_KEY)
        return make_response(jsonify(login=True, user_exists=True,  token=token), 201)
    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(error=e), 401)



# Argon2 for hashing passwords using salt
ph = PasswordHasher()

def Phash(password):
    return ph.hash(password)


def verifyPass(hash, password):
    try:
        return ph.verify(hash, password)
    except:
        return False