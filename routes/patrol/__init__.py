from functools import wraps
from config import db
import config
from flask import jsonify, make_response, request
import jwt


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
                token, config.SECRET_KEY, algorithms=["HS256"])
            current_user = db.patrol.find_one({"_id": data["public_id"]})
        except Exception as e:
            print(e,  e.__traceback__.tb_lineno)
            return make_response(jsonify({
                'message': 'unable to find patrol authority'
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
        if str(api_key) == config.API_KEY:
            # print("thank god")
            pass
        else:
            return make_response(jsonify({
                'message': 'api_key is invalid !!'
            })), 401

        # returns the current logged in users context to the routes
        return f(*args, **kwargs)
    return decorated


def Special_permissionAuth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        '''
        stuff here is validated and functions using this 
        decorater are not accessed bby anyone unless admin authority 
        basically to register all police ids
        '''
        return f(*args, **kwargs)
    return decorated
