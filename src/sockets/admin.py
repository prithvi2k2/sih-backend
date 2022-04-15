from config import socket
from flask_socketio import send
from flask import Blueprint

admin_sockets = Blueprint('admin_sockets', __name__)

@socket.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast = True)