"""Initialization of film_api package"""
import logging
import os

from flask import Flask
from flask_login import LoginManager

from film_api.database.models import init_db, User, db_session

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')

login_manager = LoginManager(app)

from film_api.blueprints.login import login
from film_api.blueprints.api_endpoints import api_blueprint, api

login_manager.login_view = 'login.login_endpoint'

app.register_blueprint(login)
app.register_blueprint(api_blueprint)

fh = logging.FileHandler("api.log")

api.logger.addHandler(fh)

if os.getenv('DEBUG'):
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    app.run()
