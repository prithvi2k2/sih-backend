# from Logic_objects import
from flask import Blueprint, request, jsonify, make_response
from itsdangerous import json
from routes.patrol import Special_permissionAuth, API_required, token_required
from config import db
from Logic_objects import file_server as logic


case = Blueprint('case', __name__)


@case.route("/get_cases", methods=['GET'])
@token_required
@API_required
def get_cases(current_user):
    if not current_user:
        return make_response(jsonify({
            'message': 'unable to find user '
        }), 400)
    try:
        # print()
        return make_response(jsonify(current_user['case_ids']))
    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(error=e), 401)


@case.route("/case_status", methods=['POST'])
@token_required
@API_required
def case_status(current_authority):
    if not current_authority:
        return make_response(jsonify({
            'message': 'unable to find user '
        }), 400)
    try:
        resp = dict(request.json)

        case_id, status = resp.get('caseID'), resp.get('status')
        if not case_id or not status:
            return make_response(jsonify(error="No Data payload!!"), 401)

        if case_id not in current_authority['case_ids']:
            return make_response(jsonify(error="Trying to update status of unassigned case"), 401)

        if status == "insufficient":
            db.reports.update_one({"_id": case_id}, {
                "$set": {"Status": "insufficient"}})
            return make_response(jsonify(msg="Status Updated")), 200
        elif status == "Assigned":
            db.reports.update_one({"_id": case_id}, {
                "$set": {"Status": "Assigned"}})
            return make_response(jsonify(msg="Status Updated")), 200

        elif status == "Resolved":
            db.reports.update_one({"_id": case_id}, {
                "$set": {"Status": "Resolved"}})

            case_info = db.reports.find_one({"_id": case_id})
            wallet_addr = case_info['wallet_addr']

            send_crypto = logic.Reward(wallet_addr)
            return_hash = send_crypto.sign_transaction()
            if not return_hash:
                return make_response(jsonify(error="unable to send cryptocurrency"))
            return make_response(jsonify(transaction_hash=return_hash))

        elif status == "Duplicate":
            db.reports.delete_one({"_id": case_id})
            return make_response(jsonify(msg="Case removed")), 200
        elif status == "Unassigned":
            db.reports.update_one({"_id": case_id}, {
                "$set": {"Status": "Unassigned",
                         "authority_assigned": None}})
            return make_response(jsonify(msg="Status Updated")), 200

    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(error=e), 401)
