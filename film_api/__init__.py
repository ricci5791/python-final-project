"""Initialization of film_api package"""

from flask import Flask
from flask_login import LoginManager

from film_api.database.models import init_db, User, db_session

app = Flask(__name__)

login_manager = LoginManager()

from film_api.blueprints.login import login

app.register_blueprint(login)


@app.route('/init_db')
def init_db_end():
    init_db()
    return '', 200


if __name__ == '__main__':
    app.run()
    init_db()
