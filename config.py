import os
from dotenv import load_dotenv

load_dotenv()

### GLOBAL SECRETS & CONSTANTS ###
MONGO_URI = os.getenv('MONGO_URI')
API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
# Get port or fallback
PORT = int(os.getenv("PORT", 8080))

### MongoDB ###
# This is seperated from main app so that it
# can be flexibly imported to blueprints without causing circular import errors

# 'db' object will initialize & refer to default database when app.py is run and
#  can be imported and used as is for DB operations
db = None