from flask import Flask
from sympy import im
from database import mongo
from dotenv import load_dotenv
import os


load_dotenv()


def create_app():
    app = Flask(__name__)

    # drop your mongoDB uri in an env file
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # Establish connection to MongoDB Cluster
    try:
        mongo
        print(' * Established connection to DB')
    except Exception as ex:
        print('Can not connect to DB=>'+str(ex))

    # Import blueprints
    from routes.USER_ROUTES import test, authenticate, crime_server
    from routes.AUTHORITY_ROUTES import authenticate as police_auth
    # Register Blueprints
    app.register_blueprint(test.test)
    app.register_blueprint(authenticate.user)
    app.register_blueprint(crime_server.file)
    app.register_blueprint(police_auth.authority)

    return app


if __name__ == '__main__':
    create_app().run(debug=True)
    # app.run(debug=True)
