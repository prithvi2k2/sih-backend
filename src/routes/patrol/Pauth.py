
import uuid
from argon2 import PasswordHasher
import jwt
from config import db
import config
from Logic_objects import location as loc
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, make_response
from routes.patrol import Special_permissionAuth, API_required, token_required


patrol = Blueprint('patrol', __name__)


@patrol.route("/signup",  methods=['POST'])
@Special_permissionAuth
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
            return make_response(jsonify(user_exists=True), 409)

        db.patrol.insert_one(auth_obj)

        return make_response(jsonify(user_exists=False), 201)
    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(error=e), 401)


@patrol.route("/login", methods=['POST'])
@API_required
def login():
    try:
        req = dict(request.json)
        AuthorityID = req.get("AuthorityID")
        location = req.get("location")
        pw = req.get("password")

        if not AuthorityID or not pw or not location:
            return make_response(jsonify(error="No Data payload!!"), 401)

        user_obj = db.patrol.find_one({"name": AuthorityID})

        if user_obj == None:
            return make_response(jsonify(login=False, user_exists=False), 401)

        if not verifyPass(user_obj["password"], pw):
            return make_response(jsonify(login=False, user_exists=True), 201)

        location = loc.Location(location)
        user_obj["location"] = location.__repr__()
        
        # jwt generation
        token = jwt.encode({
            'public_id': user_obj["_id"],
            'exp': datetime.utcnow() + timedelta(weeks=2)
        }, config.SECRET_KEY)

        db.patrol.update_one({"_id": user_obj["_id"]}, {
            "$set": {
                "location": user_obj["location"]}
        })

        return make_response(jsonify(login=True, user_exists=True,  token=token), 200)

    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(error=e), 401)


@patrol.route("update_location", methods=['POST'])
@token_required
def updateLoc(current_user):
    try:
        req = dict(request.json)
        location = req.get("location")
        if not location:
            return make_response(jsonify(error="No Data payload!!"), 401)

        location = loc.Location(location)
        current_user["location"] = location.__repr__()

        db.patrol.update_one({"_id": current_user["_id"]}, {
            "$set": {
                "location": current_user["location"]}
        })
        
        return make_response(jsonify(msg="update_success"), 200)
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
