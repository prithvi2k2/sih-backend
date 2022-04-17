from functools import wraps
from config import db
import config
from flask import jsonify, make_response, request
import jwt

# Decorators


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None

        # jwt is passed in the request header
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
            current_user = db.users.find_one({"_id": data["public_id"]})
            if not current_user:
                return make_response(jsonify({
                    'message': 'unable to find user '
                }), 404)
        except Exception as e:
            print(e,  e.__traceback__.tb_lineno)
            return make_response(jsonify({
                'message': 'unable to find user or token tampered!'
            }), 400)

        # returns the current logged in users context to the routes
        return f(current_user, *args, **kwargs)
    return decorated