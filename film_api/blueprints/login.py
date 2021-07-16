"""
Login blueprint with authorization with either username/password or api key
"""
from typing import Optional
from flask import Blueprint, request as req, make_response, abort

from film_api import login_manager
from film_api.database.models import User

login = Blueprint('login', __name__)


@login_manager.request_loader
def load_user_with_api_key(request) -> Optional[User]:
    """
    Retrieve authorization header from http request and return user if such
    exists

    :param request: Request data
    :return: User if is found
    :rtype: User
    """
    auth_header = request.headers.get('Authorization')
    api_key = auth_header.replace('X-Token ', '')

    if api_key:
        user = User.query.filter_by(api_key=api_key).first()
    else:
        user = None

    return user


@login_manager.request_loader
def load_user_with_password(request) -> Optional[User]:
    """
    Retrieve authorization header from http request and return user if such
    exists

    :param request: Request data
    :return: User if is found
    :rtype: User
    """
    login_data: dict = request.get_json()

    if login_data is None:
        return None

    username = login_data.get('username')
    password = login_data.get('password')

    user = User.query.filter_by(username=username) \
        .filter_by(password=password).first()

    return user


@login.route('/login')
def login_endpoint():
    """
    Login endpoint with either in-header token or username/password
    authorization

    :return: Return string token if login is successful, http400 otherwise
    """
    if 'Authorization' in req.headers:
        user = load_user_with_api_key(req)
    else:
        user = load_user_with_password(req)

    if user:
        return make_response(user.api_key)

    return abort(400)
