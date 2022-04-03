from flask import Flask
from routes import  test, authenticate
from database import mongo
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    # drop your mongoDB uri in an env file
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    # Establish connection to MongoDB Cluster
    try:
        mongo.init_app(app)
        print(' * Established connection to DB')
    except Exception as ex:
        print('Can not connect to DB=>'+str(ex))


    # Register Blueprints
    app.register_blueprint(test.test)
    app.register_blueprint(authenticate.user)

    return app

if __name__ == '__main__':
    create_app().run(debug=True)
    # app.run(debug=True)