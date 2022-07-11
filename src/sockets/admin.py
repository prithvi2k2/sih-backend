from argparse import Namespace
from functools import wraps
import config
import jwt
from config import socket, db
from flask_socketio import send, emit, ConnectionRefusedError
from flask import Blueprint, request
from Logic_objects.location import Location


admin_sockets = Blueprint('admin_sockets', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None

        # jwt is passed in the request header
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
                raise ConnectionRefusedError("Token tampered")
            current_user = db.admin.find_one({"_id": data["_id"]})
            # print(current_user)
            if not current_user:
                raise ConnectionRefusedError("User not found")
        except Exception as e:
            print(e,  e.__traceback__.tb_lineno)
            raise ConnectionRefusedError("errror ")

        # returns the current logged in users context to the routes
        return f(*args, **kwargs)
    return decorated


@socket.on('connect', namespace='/admin')
@token_required
def test_connect():
    print('Admin socket connection established 🤝 🤝')


@socket.on('Get_cases',  namespace='/admin')
@token_required
def handleMessage():
    cases = [reports for reports in db.reports.find()]
    emit('static-cases', cases)


@socket.on('Get_patrols',  namespace='/admin')
@token_required
def handleMessage():
    patrols = [patrol for patrol in db.patrol.find({})]
    for patrol in range(len(patrols)):
        del patrols[patrol]['password']
    emit('static-patrol', patrols)


@socket.on('Get_OnLocation', namespace='/admin')
@token_required
def handleMessage(msg):
    """
    Format 
    msg = {"location": "uppal",
            "pid": 2}
    """
    location, page = msg.get("location"), msg.get("pid")
    if not location or not page:
        emit('error_msg', {"error": "No data payload"})
        raise ConnectionRefusedError("disconnect")
    else:
        loc = Location(location)
        results = db.reports.find(
            {"location": {"$near": location.__repr__()}}).skip(10*(page - 1)).limit(page*10)
        emit('CasesUpadte', results)


@socket.on('Get_OnStatus', namespace='/admin')
@token_required
def Get_OnStatus(msg):
    """
    Format 
    msg = {"Status": "ASSIGNED",
            "pid": 2}
    """
    Status, page = msg.get("Status"), msg.get("pid")
    if not Status or not page:
        emit('error_msg', {"error": "No data payload"})
        raise ConnectionRefusedError("disconnect")
    else:
        results = db.reports.find({"Status": Status}).skip(
            10*(page - 1)).limit(page*10)
        emit('CasesUpadte', results)
    print(msg)


@socket.on('Get_OnScore', namespace='/admin')
@token_required
def Get_OnScore(msg):
    """
    PENDING AFTER ML
    """
    Score, page = msg.get("Score"), msg.get("pid")
    if not Score or not page:
        emit('error_msg', {"error": "No data payload"})
        raise ConnectionRefusedError("disconnect")
    elif Score == "High":
        db.reports.find().sort("crime_score", 1).skip(
            10*(page - 1)).limit(page*10)
    elif Score == "Low":
        db.reports.find().sort("crime_score", -1).skip(
            10*(page - 1)).limit(page*10)
    print(msg)


@socket.on('Get_OnClassified', namespace='/admin')
@token_required
def Get_Onclassified(msg):
    """
    PENDING AFTER FRONTEND AND ML
    """
    classified, page = msg.get("classified"), msg.get("pid")
    if not classified or not page:
        emit('error_msg', {"error": "No data payload"})
        raise ConnectionRefusedError("disconnect")
    else:
        results = db.reports.find({"classified_model": classified}).skip(
            10*(page - 1)).limit(page*10)
        emit('CasesUpadte', results)
    print(msg)


@socket.on_error(namespace='/admin')
def error_handler(e):
    print('/admin SocketIO error : ' + str(e))

@socket.on('disconnect', namespace='/admin')
@token_required
def test_connect():
    print('Broooo 💔 - Admin socket closed')
