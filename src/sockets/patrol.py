from config import socket, db
import config
from flask_socketio import send, emit, ConnectionRefusedError
from flask import Blueprint, request
from functools import wraps
import jwt
import time
import pymongo
import logging
patrol_sockets = Blueprint('patrol_sockets', __name__)


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
            current_user = db.patrol.find_one({"_id": data["public_id"]})
            # print(current_user)
            if not current_user:
                raise ConnectionRefusedError("User not found")
        except Exception as e:
            print(e,  e.__traceback__.tb_lineno)
            raise ConnectionRefusedError("errror ")
            return e

        # returns the current logged in users context to the routes
        return f(current_user, *args, **kwargs)
    return decorated


@socket.on('connect',  namespace='/patrol')
@token_required
def test_connect(current_user):
    if current_user is None:
        raise ConnectionRefusedError("errror ")
    else:
        print('Patrol socket connection established 🤝')


@socket.on('Get_cases',  namespace='/patrol')
@token_required
def handleMessage(current_user, msg):
    """
    msg = {}
    """
    print(current_user, msg)
    # pipeline =
    # with db.patrol.watch(query) as watch:
    emit('CasesUpadte', current_user['case_ids'])

    # try:
    resume_token = None
    pipeline = [
        {
            '$match': {
                '_id': current_user['_id']}
        }
    ]
    with db.patrol.watch(pipeline) as stream:
        for insert_change in stream:
            print(insert_change)
            resume_token = stream.resume_token

    resume_token = None
    try:
        with db.collection.watch(pipeline) as stream:
            for insert_change in stream:
                emit('CasesUpadte', current_user['case_ids'])
                resume_token = stream.resume_token
    except pymongo.errors.PyMongoError:
        if resume_token is None:
            logging.error('...')
        else:
            with db.collection.watch(
                    pipeline, resume_after=resume_token) as stream:
                for insert_change in stream:
                    emit('CasesUpadte', current_user['case_ids'])

       # pass


@socket.on('disconnect',  namespace='/patrol')
@token_required
def test_connect(current_user):
    print('Broooo 💔 - Patrol socket closed')
