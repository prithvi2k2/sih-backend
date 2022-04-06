import jwt
from argon2 import PasswordHasher
from hashlib import sha256
from config import db
import config
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, make_response

from routes.users import API_required, token_required


user = Blueprint('user', __name__)


@user.route("/signup",  methods=['POST'])
@API_required
def signup():
    try:
        req = dict(request.json)
        user = req.get("user")
        password = req.get("password")
        if not user or not password:
            return make_response(jsonify(error="Username and Password REQUIRED"), 400)

        user_hash = Uhash(user)

        user_obj = db.users.find_one({"_id": user_hash})

        if user_obj != None:
            return make_response(
                jsonify(user_exists=True,
                        message="Username already taken"), 409)

        user_obj = {
            "_id": user_hash,
            "wallet_addr": req.get('wallet_addr'),
            "password": Phash(password),
            "case_ids": []
        }
        db.users.insert_one(user_obj)

        return make_response(jsonify(user_exists=False, message="User registered"), 201)

    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(error=e), 401)


@user.route("/login", methods=['POST'])
@API_required
def login():
    try:
        req = dict(request.json)
        user = req.get("user")
        password = req.get("password")
        if not user or not password:
            return make_response(jsonify(error="Username and Password REQUIRED"), 400)

        user_hash = Uhash(user)

        user_obj = db.users.find_one({"_id": user_hash})

        if user_obj == None:
            return make_response(jsonify(user_exists=False, login=False, token=None), 401)

        if not verifyPass(user_obj["password"], password):
            return make_response(
                jsonify(message="Incorrect Password",
                        login=False, user_exists=True, token=None), 401)

        token = jwt.encode({
            'public_id': user_obj["_id"],
            'exp': datetime.utcnow() + timedelta(weeks=2)
        }, config.SECRET_KEY)
        return make_response(
            jsonify(login=True, user_exists=True,  token=token), 200)
    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(error=e), 401)


@user.route('/change_wallet', methods=['POST'])
@API_required
@token_required
def change_wallet(current_user):
    try:
        data = dict(request.json)
        new_addr = data.get("new_addr")
        current_user["wallet_addr"] = new_addr
        del current_user["password"]
        db.users.update_one({"_id": current_user["_id"]}, {
            "$set": {
                "wallet_addr": current_user["wallet_addr"]}
        })
        return jsonify(current_user)
    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(error=e), 401)


# default route to authenticate or for init after re-opening client
@user.route('/init')
@API_required
@token_required
def init(current_user):
    print(current_user)
    return "reyy"


@user.route('/Get_UserCases',  methods=['GET'])
@API_required
@token_required
def Get_UserCases(current_user):
    return make_response(jsonify(cases=current_user["case_ids"]))


# SHA256 for hashing usernames
def Uhash(username):
    return sha256(username.encode('utf-8')).hexdigest()


# Argon2 for hashing passwords using salt
ph = PasswordHasher()


def Phash(password):
    return ph.hash(password)


def verifyPass(hash, password):
    try:
        return ph.verify(hash, password)
    except:
        return False
