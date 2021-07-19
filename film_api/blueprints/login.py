"""
Login blueprint with authorization with either username/password or api key
"""
from typing import Optional
from flask import Blueprint, request, redirect, url_for
from flask_login import login_user

from film_api import login_manager
from film_api.database.models import User, db_session
from film_api.database.db_worker import DBWorker

login = Blueprint('login', __name__)


@login_manager.user_loader
def load_user(api_key):
    """
    Retrieve api key for the given user

    :param api_key: Api key of the user
    :return: User instance
    """
    return DBWorker.get_user_by_api_key(api_key)


@login_manager.request_loader
def load_user_with_password() -> Optional[User]:
    """
    Retrieve authorization header from http request and return user if such
    exists

    :return: User if is found
    :rtype: User
    """
    if request.headers.get('Authorization'):
        auth_header = request.headers.get('Authorization')
        api_key = auth_header.replace('X-Token ', '')

        if api_key:
            user = DBWorker.get_user_by_api_key(api_key)
        else:
            user = None

    else:
        login_data: dict = request.get_json()

        if login_data is None:
            return None

        username = login_data.get('username')
        password = login_data.get('password')

        user = DBWorker.get_user_by_creds(username, password)

    if user:
        login_user(user, remember=True)
        user.is_authenticated = True
        db_session.commit()

    return user


@login.route('/login')
def login_endpoint():
    """
    Login endpoint with either in-header token or username/password
    authorization

    :return: Return string token if login is successful, http400 otherwise
    """
    user = load_user_with_password()

    if user:
        next_url = request.args.get('next')
        if next_url:
            return redirect(url_for(f'api_endpoints.{next_url[1:] or ""}'))
        return 'User has been loaded', 200
    return 'User with provided credentials was not found', 401
