
from functools import wraps
import mimetypes
from tkinter.messagebox import NO
from flask import Blueprint, request, current_app, make_response, jsonify
import os
import uuid
from routes import client
import json

from matplotlib.font_manager import json_dump
from file_server import server


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
            db = client['research']
            collection = db["research_auth"]
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
def live():
    """
    Format of data intake

    json = {
        desc : str : data,
        victims : str names,
        ofenders : str names,
        location : str loc,
        time : object Datetime()
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
        crime_id = uuid.uuid4()

        payload = dict(request.files)
        data = json.load(payload["data"])
        del payload["data"]

        files = []
        for v in payload.values():
            file_type = mimetypes.guess_type(v.filename)[0].split("/")[0]
            file = v
            save_file = server.File_server(file_type)
            filename = save_file.save_file(v)
            if filename:
                files.append([filename, file_type])

        desc, victims, ofenders, location, time = data.get("desc", None), data.get(
            "victims", None), data.get("ofenders", None), data.get("location", None), data.get("time", None)
        print(desc, victims, ofenders, location, time)

        crime_obj = {
            "_id": crime_id,
            "desc": desc,
            "victims": victims,
            "ofenders": ofenders,
            "location": location,
            "time": time,
            "crime_files": files,
            "crime_score": None,
            "classification": None
        }

        db = client['crimes']
        collection = db["crimes"]
        collection.insert_one(crime_obj)
        # print(files)
        return make_response(jsonify(uploaded="sucess")), 200
    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(uploaded="fail", file_id=None, error=e)), 403
