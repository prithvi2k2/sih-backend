""""
Handles reports/cases uploaded by citizens

"""
import mimetypes
import enum
import uuid
import json
from config import db
from Logic_objects import location as loc
from ML_workspace import model
from Logic_objects import file_server
from flask import Blueprint, request, make_response, jsonify

from routes.users import token_required
from routes import API_required


class STATUS(enum.Enum):
    insufficient = 1
    Unassigned = 2
    Assigned = 3
    Resolved = 4
    Duplicate = 5


file = Blueprint('file', __name__)


@file.route("/new-report",  methods=['POST'])
@token_required
@API_required
def new_report(current_user):
    if not current_user:
        return make_response(jsonify({
            'message': 'unable to find user '
        }), 400)
    """
    Format of data intake

    json = {
        desc : str : data,
        victims : str names,
        offenders : str names,
        location : str loc,
        time : object Datetime()
        type : str crime_type
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
        data = dict(request.json)

        desc, victims, ofenders, location, time, classified_ByUser, files = data.get("desc"), data.get(
            "victims"), data.get("ofenders"), data.get("location"), data.get("time"), data.get("classified_ByUser"), data.get("files")
        # print(desc, victims, ofenders, location, time)

        if not desc or not location or not time:
            return make_response(jsonify(error="No Data payload!!"), 401)

        file = []
        for k, v in files.items():
            file.append([k, v])

        """
        if files in data uncomment and use this
        """
        # for v in payload.values():
        #     file_type = mimetypes.guess_type(v.filename)[0].split("/")[0]
        #     file = v
        #     save_file = file_server.File_server(file_type)
        #     filename = save_file.save_file(v)
        #     if filename:
        #         files.append([filename, file_type])

        location = loc.Location(location)
        print(location.__repr__(),  "\n\n")
        if not location.__repr__():
            return make_response(jsonify(error="Cannot find the location specified!!"), 404)

        # finding nearest police station
        authority_assigned = db.patrol.find(
            {"location": {"$near": location.__repr__()}}).limit(1)

        print(authority_assigned[0]["_id"])
        crime_obj = {
            "_id": crime_id,
            "desc": desc,
            "victims": victims,
            "offenders": ofenders,
            "location": location.__repr__(),
            "time": time,
            "crime_files": file,
            "crime_score": None,
            "classified_model": None,
            "faces_bymodel": [],
            "Status": "Assigned",
            "wallet_addr": current_user["wallet_addr"],
            "authority_assigned": authority_assigned[0]["_id"]
        }

        db.reports.insert_one(crime_obj)
        # print(files)
        model.Model(crime_obj=crime_obj)

        current_user["case_ids"].append(crime_id)
        db.users.update_one({"_id": current_user["_id"]}, {
            "$set": {"case_ids": current_user["case_ids"]}})

        cases = authority_assigned[0]['case_ids']
        cases.append(crime_id)
        task = db.patrol.update_one({"_id": authority_assigned[0]["_id"]}, {
            "$set": {"case_ids": cases}})

        return make_response(jsonify(uploaded="success", user_cases=current_user["case_ids"]), 201)

    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(uploaded="fail", file_id=None, error=e), 403)


@file.route("/get-case-info",  methods=['POST'])
@token_required
@API_required
def get_case(current_user):
    try:
        data = dict(request.json)
        case_id = data.get("case_id")

        case_info = db.reports.find_one({"_id": case_id})
        if not case_info:
            return make_response(jsonify(case_found=False, case_info=None))
        del case_info['wallet_addr']

        return make_response(jsonify(case_found=True, case_info=case_info), 200)

    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(uploaded="fail", file_id=None, error=e), 403)


@file.route("/emergency", methods=['POST'])
@token_required
@API_required
def emergency(current_user):
    try:
        crime_id = str(uuid.uuid4())
        data = dict(request.json)
        location = data.get("location")

        if not location:
            return make_response(jsonify(error="No Location specified!!"), 401)

        location = loc.Location(location)
        if not location.__repr__():
            return make_response(jsonify(error="Cannot find the location specified!!"), 404)

        # finding nearest 4 authorities, a dictionary obj
        nearest_authoritiesObj = db.patrol.find(
            {"location": {"$near": location.__repr__()}}).limit(4)
        
        nearest_authorityID = nearest_authoritiesObj[0]['_id']
        nearest_authoritiesIds = [authority['_id'] for authority in nearest_authoritiesObj]
        
        crime_obj = {
            "_id": crime_id,
            "location": location.__repr__(),
            "emergency": True,
            "Status": "Assigned",
            "wallet_addr": current_user["wallet_addr"],
            "nearest_authority": nearest_authorityID,
            "nearest_authorities": nearest_authoritiesIds
        }
        
        db.reports.insert_one(crime_obj)
        
        model.Model(crime_obj=crime_obj)

        current_user["case_ids"].append(crime_id)
        db.users.update_one({"_id": current_user["_id"]}, {
            "$set": {"case_ids": current_user["case_ids"]}})
        
        for authority in nearest_authoritiesObj:
            cases = authority['case_ids']
            cases.append(crime_id)
            db.patrol.update_one({"_id": authority['_id']}, {
                "$set": {"case_ids": cases}})

        return make_response(jsonify(nearest_authority= nearest_authorityID,
                nearest_authorities=nearest_authoritiesIds), 201)

    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(uploaded="fail", error=e), 400)
