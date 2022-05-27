'''
MONGO ATLAS TRIGGERS FOR REAL-TIME UPDATES TO SOCKETS
'''
from functools import wraps
from flask import jsonify, make_response, request, Blueprint
from config import socket
import config


triggers = Blueprint('triggers', __name__)


def API_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'X-API-Key' in request.headers:
            api_key = request.headers['X-API-Key']
        if not api_key:
            return make_response(jsonify({"message": "API-KEY is missing !!"}), 400)
        if str(api_key) == config.API_KEY:
            pass
        else:
            return make_response(jsonify({
                'message': 'API_KEY is invalid !!'
            }), 401)

        return f(*args, **kwargs)
    return decorated


@triggers.route('/p/cases-add-del', methods=['POST'])
@API_required
def patrolUpdateCases():
    '''
    Triggered whenever 'case_ids' field of a patrol document is UPDATEd
    either cases `added/inserted` or `removed/deleted`
    '''
    changes = dict(request.json)
    room = changes['_id']
    socket.emit('CaseUpdate', changes, namespace='/patrol', to=room)
    socket.emit('PatrolUpdate', changes, namespace='/admin')
    return make_response("success", 200)


@triggers.route('/a/cases-add-del', methods=['POST'])
@API_required
def adminUpdateCases():
    '''
    Triggered whenever REPORTS collection undergoes following operations
    either cases `added/inserted` or `removed/deleted` or `modified/updated`
    '''
    changes = dict(request.json)
    socket.emit('CaseUpdate', changes, namespace='/admin')
    return make_response("success", 200)


# @triggers.route('/active-patrol', methods=['POST'])
# @API_required
# def activePatrol():
#     req = dict(request.json)


# @triggers.route('/', methods=['POST'])
# @API_required
# def f():
#     pass

