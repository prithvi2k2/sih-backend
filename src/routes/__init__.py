from functools import wraps
import config
from flask import jsonify, make_response, request
from hashlib import sha256
from argon2 import PasswordHasher


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


# SHA256 for hashing usernames
def Uhash(username):
    return sha256(username.encode('utf-8')).hexdigest()


# Argon2 for hashing passwords using salt
ph = PasswordHasher()

def Phash(password):
    return ph.hash(password)

def verifyPass(hash, password):
    try:
        return ph.verify(hash, password)
    except:
        return False
