from argparse import Namespace
from config import socket, db
from flask_socketio import send, emit, ConnectionRefusedError
from flask import Blueprint, request
from Logic_objects.location import Location


admin_sockets = Blueprint('admin_sockets', __name__)


@socket.on('connect')
def test_connect():
    print('Broo connection established 🤝 🤝')


@socket.on('Get_OnLocation')
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


@socket.on('Get_OnStatus')
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


@socket.on('Get_OnScore')
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


@socket.on('Get_Onclassified')
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


@ socket.on('disconnet')
def test_connect():
    print('Broooo 💔')
