from datetime import datetime, timedelta
import jwt
from routes import API_required, verifyPass
from routes.admin import token_required
from flask import Blueprint, request, jsonify, make_response
from config import db
import config


admin = Blueprint('admin', __name__)


@admin.route("/login", methods=['POST'])
@API_required
def login():
    try:
        req = dict(request.json)
        uid = req.get("user")
        pw = req.get("password")

        if not uid or not pw:
            return make_response(jsonify(error="No Data payload!!"), 401)

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


@admin.route("/get_cases")
@token_required
@API_required
def getCases(*args):
    try:
        reports = list(db.reports.find())
        return make_response(jsonify(reports), 200)
    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(error=e), 404)
