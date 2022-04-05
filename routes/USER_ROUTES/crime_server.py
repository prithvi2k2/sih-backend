from functools import wraps
import mimetypes
import enum
from operator import mod
import os
import uuid
import json
import jwt

from Logic_objects import location as loc
from ML_workspace import model
from routes.USER_ROUTES import client
from Logic_objects import file_server
from flask import Blueprint, request, current_app, make_response, jsonify


class STATUS(enum.Enum):
    insufficient = 1
    Unassigned = 2
    Inprogress = 3
    Resolved = 4
    Duplicate = 5


file = Blueprint('file', __name__)
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


@file.route("/upload_Data",  methods=['POST'])
@token_required
@API_required
def live(current_user):
    """
    Format of data intake

    json = {
        desc : str : data,
        victims : str names,
        ofenders : str names,
        location : str loc,
        time : object Datetime()
        classified_ByUser : str crime_type
    }

    file = {
        file1 : [data , type]
          *         *
          *         *
          *         *
          *         *
    }
    """

    try:
        crime_id = str(uuid.uuid4())

        payload = dict(request.files)
        data = json.load(payload["data"])
        del payload["data"]
        desc, victims, ofenders, location, time, classified_ByUser = data.get("desc", None), data.get(
            "victims", None), data.get("ofenders", None), data.get("location", None), data.get("time", None), data.get("classified_ByUser", None)
        # print(desc, victims, ofenders, location, time)
        if not desc or not location or not time:
            return make_response(jsonify(error="No Data payload!!")), 401

        files = []
        for v in payload.values():
            file_type = mimetypes.guess_type(v.filename)[0].split("/")[0]
            file = v
            save_file = file_server.File_server(file_type)
            filename = save_file.save_file(v)
            if filename:
                files.append([filename, file_type])
        location = loc.Location(location)
        print(location.__repr__(),  "\n\n")
        if not location.__repr__():
            return make_response(jsonify(error="Cannot find the location specifies!!"))

        # finding nearest polices station
        collection = client["crimes"]["Authority_auth"]
        authority_assigned = collection.find(
            {"location": {"$near": location.__repr__()}}).limit(1)
        print(authority_assigned[0]["_id"])
        crime_obj = {
            "_id": crime_id,
            "desc": desc,
            "victims": victims,
            "ofenders": ofenders,
            "location": None,
            "time": time,
            "crime_files": files,
            "crime_score": None,
            "classified_ByUser": classified_ByUser,
            "classified_model": None,
            "faces_bymodel": [],
            "Status": "Unassigned",
            "wallet_addr": current_user["wallet_addr"],
            "authority_assigned": authority_assigned[0]["_id"]
        }

        db = client['crimes']
        collection = db["crimes"]
        collection.insert_one(crime_obj)
        # print(files)
        model.Model(crime_obj=crime_obj)

        current_user["case_ids"].append(crime_id)
        db = client['crimes']
        collection = db["crimes_auth"]
        collection.update_one({"_id": current_user["_id"]}, {
            "$set": {"case_ids": current_user["case_ids"]}})
        return make_response(jsonify(uploaded="sucess", user_cases=current_user["case_ids"])), 200
    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(uploaded="fail", file_id=None, error=e)), 403


@file.route("/Get_CaseInfo",  methods=['POST'])
@token_required
@API_required
def get_case(current_user):
    try:
        data = dict(request.json)
        case_id = data.get("case_id", None)

        db = client['crimes']
        collection = db["crimes"]
        case_info = collection.find_one({"_id": case_id})
        if not case_info:
            return make_response(jsonify(case_found=False, case_info=None))
        del case_info['wallet_addr']

        return make_response(jsonify(case_found=True, case_info=case_info)), 200

    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(uploaded="fail", file_id=None, error=e)), 403
