"""
The built-in Flask server is not meant to be used in a production environment
as their official docs also state that it isn't stable, efficient and scalable and
to use a proper production-ready WSGI server

'waitress' is a lightweight WSGI server

This script is run in a production environment.
"""

from waitress import serve
from app import create_app
import logging
import config

APP = create_app()

logger = logging.getLogger('waitress')
logger.setLevel(logging.DEBUG)

serve(APP, port=config.PORT)