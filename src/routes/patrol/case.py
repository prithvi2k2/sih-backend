# from Logic_objects import
from flask import Blueprint, request, jsonify, make_response
from routes.patrol import Special_permissionAuth, token_required
from routes import API_required
from config import db
from Logic_objects import reward_crypto


case = Blueprint('case', __name__)


@case.route("/get-cases", methods=['GET'])
@token_required
@API_required
def get_cases(current_user):
    if not current_user:
        return make_response(jsonify({
            'message': 'unable to find user'
        }), 404)
    try:
        # print()
        return make_response(jsonify(cases=current_user['case_ids']))
    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(error=e), 401)


@case.route("/case-status", methods=['POST'])
@token_required
@API_required
def case_status(current_authority):
    if not current_authority:
        return make_response(jsonify({
            'message': 'unable to find user '
        }), 404)
    try:
        req = dict(request.json)

        case_id, status = req.get('caseID'), req.get('status')
        if not case_id or not status:
            return make_response(jsonify(error="No Data payload!!"), 400)

        if case_id not in current_authority['case_ids']:
            return make_response(jsonify(error="Trying to update status of unassigned case"), 404)

        if status == "insufficient":
            db.reports.update_one({"_id": case_id}, {
                "$set": {"Status": "insufficient"}})
            return make_response(jsonify(msg="Status Updated"), 200)
        elif status == "Assigned":
            db.reports.update_one({"_id": case_id}, {
                "$set": {"Status": "Assigned"}})
            return make_response(jsonify(msg="Status Updated"), 200)

        elif status == "Resolved":
            db.reports.update_one({"_id": case_id}, {
                "$set": {"Status": "Resolved"}})

            case_info = db.reports.find_one({"_id": case_id})
            wallet_addr = case_info['wallet_addr']

            send_crypto = reward_crypto.Reward(wallet_addr)
            return_hash = send_crypto.sign_transaction()
            if not return_hash:
                return make_response(jsonify(error="unable to send cryptocurrency"))
            return make_response(jsonify(transaction_hash=return_hash))

        elif status == "Duplicate":
            db.reports.delete_one({"_id": case_id})
            return make_response(jsonify(msg="Case removed"), 204)
        elif status == "Unassigned":
            db.reports.update_one({"_id": case_id}, {
                "$set": {"Status": "Unassigned",
                         "authority_assigned": None}})
            return make_response(jsonify(msg="Status Updated"), 200)

    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(error=e), 401)
