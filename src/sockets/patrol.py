from config import socket, db
import config
from flask_socketio import send, emit, join_room, ConnectionRefusedError
from flask import Blueprint, jsonify, make_response, request
from functools import wraps
import jwt


patrol_sockets = Blueprint('patrol_sockets', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None

        # jwt is passed in the extraHeaders while opening WS connection
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            raise ConnectionRefusedError("Auth Token missing")

        # jwt validation
        try:
            try:
                data = jwt.decode(
                    token, config.SECRET_KEY, algorithms=["HS256"])
            except Exception as e:
                raise ConnectionRefusedError("Token tampered/expired")
            current_user = db.patrol.find_one({"_id": data["public_id"]})
            # print(current_user)
            if not current_user:
                raise ConnectionRefusedError("User not found")
        except Exception as e:
            print(e,  e.__traceback__.tb_lineno)
            raise ConnectionRefusedError("errror ")

        # returns the current logged in users context to the routes
        return f(current_user, *args, **kwargs)
    return decorated


@socket.on('connect',  namespace='/patrol')
@token_required
def test_connect(current_user):
    if current_user is None:
        raise ConnectionRefusedError("errror ")
    else:
        join_room(current_user['_id'])
        db.patrol.update_one(
            {"_id":current_user['_id']},
            {'$inc': {'isOnline': 1}})
        print('Patrol socket connection established 🤝')


@socket.on('Get_cases',  namespace='/patrol')
@token_required
def handleMessage(current_user):
    emit('static-cases', current_user['case_ids'], to=current_user['_id'])


@socket.on_error(namespace='/patrol')
def error_handler(e):
    print('/patrol SocketIO error : ' + str(e))


@socket.on('disconnect',  namespace='/patrol')
@token_required
def test_connect(current_user):
    db.patrol.update_one(
            {'_id':current_user['_id']},
            {'$inc': {'isOnline': -1}})
    print('Broooo 💔 - Patrol socket closed')