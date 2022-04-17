"""
While lightweight and easy to use, Flask's built-in server 
is not suitable for production as it doesn't scale well

We use 'waitress' or 'gunicorn' WSGI for production
"""

from flask import Flask
import config
from flask_socketio import SocketIO

def create_app():
    app = Flask(__name__)

    # Establish connection to MongoDB Cluster
    try:
        from pymongo import MongoClient, GEO2D
        # drop your mongoDB uri as MONGO_URI in an env file
        client = MongoClient(config.MONGO_URI, connect=False)
        # Connecting to main database client["DATABASE_NAME"]
        config.db = client["secrep"]
        config.db.patrol.create_index([("location", GEO2D)])
        print(config.db)
        print(' * Established connection to DB *')
    except Exception as ex:
        print('Can not connect to DB=>'+str(ex))

    # Config websocket with app, also enables CORS
    config.socket = SocketIO(app, cors_allowed_origins='*')

    # Import blueprints
    from routes import test
    from routes.users import Uauth, reports
    from routes.patrol import Pauth
    from routes.patrol import case
    from routes.admin import admin
    from sockets.admin import admin_sockets

    # Register Blueprints
    app.register_blueprint(test.test)
    app.register_blueprint(Uauth.user)
    app.register_blueprint(reports.file)
    app.register_blueprint(Pauth.patrol, url_prefix='/patrol')
    app.register_blueprint(case.case, url_prefix='/patrol')
    app.register_blueprint(admin.admin, url_prefix='/admin')
    app.register_blueprint(admin_sockets)


    return app


if __name__ == '__main__':
    # Run this script only in development
    # Use 'waitress' or 'gunicorn' WSGI for production instead
    app = create_app()
    # Run app with SocketIO to add support for websockets
    config.socket.run(app, port=config.PORT, debug=True)
