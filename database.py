# This file is seperated from main app so that mongo.db object can be flexibly imported to blueprints without causing import errors
from flask_pymongo import PyMongo

mongo = PyMongo()