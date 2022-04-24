
import jwt
from config import db
import config
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, make_response
from routes.users import token_required
from routes import API_required, Uhash, Phash, verifyPass

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

        resp = make_response(
            jsonify(user_exists=False, message="User registered"), 201)
        return resp

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
            return make_response(jsonify(login=False, user_exists=False), 401)

        if not verifyPass(user_obj["password"], password):
            return make_response(
                jsonify(message="Incorrect Password",
                        login=False, user_exists=True), 401)

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
@token_required
@API_required
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
@token_required
@API_required
def init(current_user):
    print(current_user)
    return "reyy"


@user.route('/del-acct', methods=['DELETE'])
@token_required
@API_required
def DelAccount(current_user):
    try:
        db.users.delete_one({"_id": current_user['_id']})
        return make_response(jsonify(accountDel=True))
    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(error=e), 401)


@user.route('/Get_UserCases',  methods=['GET'])
@token_required
@API_required
def Get_UserCases(current_user):
    return make_response(jsonify(cases=current_user["case_ids"]))
