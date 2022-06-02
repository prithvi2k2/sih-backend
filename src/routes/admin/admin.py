from datetime import datetime, timedelta
import jwt
from routes import API_required, verifyPass, Phash
from routes.admin import token_required
from flask import Blueprint, request, jsonify, make_response
from config import db
import config
from Logic_objects import location as loc


admin = Blueprint('admin', __name__)


@admin.route("/login", methods=['POST'])
@API_required
def login():
    try:
        req = dict(request.json)
        uid = req.get("user")
        pw = req.get("password")

        if not uid or not pw:
            return make_response(jsonify(error="No Data payload!!"), 400)

        admin_obj = db.admin.find_one({"_id": uid})

        if admin_obj == None:
            return make_response(jsonify(login=False, user_exists=False), 401)

        if not verifyPass(admin_obj["password"], pw):
            return make_response(
                jsonify(message="Incorrect Password",
                        login=False, user_exists=True), 401)

        # jwt generation
        token = jwt.encode({
            '_id': admin_obj["_id"],
            'exp': datetime.utcnow() + timedelta(weeks=2)
        }, config.SECRET_KEY)

        return make_response(jsonify(login=True, user_exists=True,  token=token), 200)

    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(error=e), 401)


@admin.route("/get-cases")
@token_required
@API_required
def getCases(*args):
    try:
        reports = list(db.reports.find())
        return make_response(jsonify(cases=reports), 200)
    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(error=e), 404)

'''
MANAGE PATROL
'''

@admin.route("/add-patrol",  methods=['POST'])
@API_required
@token_required
def signup(_):
    try:
        req= dict(request.json)
        PatrolID = req.get("PatrolID")
        location = req.get("location")
        pw = req.get("password")
        if not PatrolID or not pw or not location:
            return make_response(jsonify(error="No Data payload!!"), 400)

        user_obj = db.patrol.find_one({"_id": PatrolID})
        if user_obj != None:
            return make_response(jsonify(user_exists=True), 409)

        location = loc.Location(location)
        if not location.__repr__():
            return make_response(jsonify(error="Cannot find the location specified!!"), 404)
        auth_obj = {
            "_id": PatrolID,
            "password": Phash(pw),
            "location": location.__repr__(),
            "case_ids": [],
            "isOnline": 0
        }

        db.patrol.insert_one(auth_obj)

        return make_response(jsonify(user_exists=False), 201)
    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(error=str(e)), 400)


@admin.route("del-patrol", methods=['DELETE'])
@token_required
@API_required
def DELpolice(_):
    try:
        req = dict(request.json)
        patrol = db.patrol.find_one({"_id": req["PatrolID"]})
        if patrol:
            for i in patrol['case_ids']:
                db.reports.update_one({"_id": i}, {
                    "$set": {"Status": "Unassigned",
                             "authority_assigned": None}})
        else:
            return make_response(jsonify(error="PatrolID not found"), 404)

        db.patrol.delete_one({"_id": patrol['_id']})
        return make_response(jsonify(accountDel=True))
    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(error=str(e)), 400)
