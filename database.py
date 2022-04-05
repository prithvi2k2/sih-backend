# This file is seperated from main app so that mongo.db object can be flexibly imported to blueprints without causing import errors
from pymongo import MongoClient, GEO2D
import os
from dotenv import load_dotenv
mongo = MongoClient(os.getenv("MONGO_URI"))
mongo["crimes"]["Authority_auth"].create_index([("location", GEO2D)])
