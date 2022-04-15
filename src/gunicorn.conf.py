'''
Using gunicorn as `production` server
This is a config file for gunicorn
'''
import os

_PORT = int(os.getenv("PORT", 8080))
bind = f'0.0.0.0:{_PORT}'

workers = 1
worker_class = 'eventlet'

errorlog = '-'
loglevel = 'info'