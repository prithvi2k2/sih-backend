import os
from dotenv import load_dotenv

load_dotenv()

### GLOBAL SECRETS & CONSTANTS ###
MONGO_URI = os.getenv('MONGO_URI')
API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
GANACHE_URL = os.getenv('GANACHE_URL')
CONTRACT = os.getenv('CONTRACT')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
# Get port or fallback
PORT = int(os.getenv("PORT", 3000))

### Global Objects ###
# Thess are seperated from main app so that they can be flexibly
# imported to blueprints without causing any circular import errors/problems

# 'db' object will initialize & refer to default database when app.py is run
db = None

# 'socket' is the SocketIO server object, initialised in app.py
socket = None
