
from flask import Flask
import config
from flask_ngrok import run_with_ngrok
from flask_cors import CORS
from flask_socketio import SocketIO


def create_app():
    app = Flask(__name__)

    # run_with_ngrok(app)
    # CORS(app)

    # Establish connection to MongoDB Cluster
    try:
        from pymongo import MongoClient, GEO2D
        # drop your mongoDB uri as MONGO_URI in an env file
        client = MongoClient(config.MONGO_URI)
        # Connecting to main database client["DATABASE_NAME"]
        config.db = client["secrep"]
        config.db.patrol.create_index([("location", GEO2D)])

        print(config.db)
        print(' * Established connection to DB *')
    except Exception as ex:
        print('Can not connect to DB=>'+str(ex))

    # Import blueprints
    from routes import test
    from routes.users import Uauth, reports
    from routes.patrol import Pauth
    from routes.patrol import case

    # Register Blueprints
    app.register_blueprint(test.test)
    app.register_blueprint(Uauth.user)
    app.register_blueprint(reports.file)
    app.register_blueprint(Pauth.patrol, url_prefix='/patrol')
    app.register_blueprint(case.case, url_prefix='/patrol')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
