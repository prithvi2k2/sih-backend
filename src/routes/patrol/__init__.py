from functools import wraps
from config import db
import config
from flask import jsonify, make_response, request
import jwt


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None

        # jwt obtained the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return make_response(jsonify({'message': 'Token is missing !!'}), 400)

        # jwt validation
        try:
            try:
                data = jwt.decode(
                    token, config.SECRET_KEY, algorithms=["HS256"])
            except Exception as e:
                return make_response(jsonify({
                    'message': 'Token invalid or tampered!! Access denied'
                }), 401)
            current_user = db.patrol.find_one({"_id": data["public_id"]})
            if not current_user:
                return make_response(jsonify({
                    'message': 'unable to find patrol authority'
                }), 404)
        except Exception as e:
            print(e,  e.__traceback__.tb_lineno)
            return make_response(jsonify({
                'message': 'unable to find patrol or token tampered!'
            }), 400)

        # returns the current logged in users context to the routes
        return f(current_user, *args, **kwargs)
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
