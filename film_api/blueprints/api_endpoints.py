"""Module with blueprint of api endpoints"""
import datetime

import flask_login
from flask import Blueprint, request
from flask_restx import Resource, Api

from film_api.checkers.film_checker import FilmChecker
from film_api.database.db_worker import DBWorker
from film_api.database.models import Film, db_session

api_blueprint = Blueprint('api_endpoints', __name__)

api = Api(api_blueprint)


@api.route('/film', methods=['GET', 'POST'])
@api.route('/film/<int:film_id>', methods=['GET', 'PATCH', 'DELETE'])
class FilmEndpoint(Resource):
    """film endpoints class"""

    @flask_login.login_required
    def get(self, film_id=None):
        """
        Get endpoint for film retrieval with specific parameters like genre,
        director name, surname, release date range and sorting by dates and
        rating

        :param film_id: Film id to be looked (Optional)
        :return: HTTP response of films in json
        """
        film_title = request.args.get('title')
        genre = request.args.get('genre')
        director_name = request.args.get('director_name')
        director_surname = request.args.get('director_surname')
        release_date_range = request.args.get('release_date')
        sort_dates = request.args.get('sort_dates')
        sort_rating = request.args.get('sort_rating')

        if film_title is None and film_id is None:
            return 'Wrong input. Provide either id or title of a film', 400

        if film_id:
            film_query = DBWorker.get_film_by_id(film_id)
            return str([film.to_json() for film in film_query.all()]), 200

        film_query = DBWorker.get_film_by_title(film_title)

        if director_name is not None or director_surname is not None:
            film_query = DBWorker.filter_film_by_director(film_query,
                                                          director_name,
                                                          director_surname)

        if genre:
            film_query = DBWorker.filter_film_by_genre(film_query, genre)

        if release_date_range:
            start_date, end_date = release_date_range.split(',')[:2]

            film_checker = FilmChecker()

            film_checker.check_date(start_date)
            film_checker.check_date(end_date)

            if not film_checker.is_correct():
                return str(film_checker.errors), 400

            film_query = DBWorker.filter_film_by_release_date(film_query,
                                                              start_date,
                                                              end_date)

        if sort_dates is not None or sort_rating is not None:
            if sort_dates is not None:
                sort_dates = int(sort_dates)
            if sort_rating is not None:
                sort_rating = int(sort_rating)

            film_query = DBWorker.sort_film(film_query, sort_dates, sort_rating)

        if film_query:
            return str([film.to_json() for film in film_query.all()]), 200

        return f'Film with id "{film_id}" or title "{film_title}" was not found', \
               404

    @flask_login.login_required
    def post(self):
        """
        Post endpoint to add film information to the db

        :return: HTTP response with status code
        """
        film_data = dict(request.get_json())
        film_checker = FilmChecker()

        is_correct, errors = film_checker.start_validation(film_data)

        if not is_correct:
            return str(errors), 400

        film = Film(film_data['film_title'],
                    datetime.datetime.strptime(film_data['release_date'],
                                               '%Y-%m-%d'),
                    film_data['poster'], film_data['created_by'],
                    film_data['producer_id'], film_data['description'],
                    film_data['rating'])

        db_session.add(film)
        db_session.commit()

        return f'film has been added with id {film.film_id}', 200

    @flask_login.login_required
    def patch(self, film_id):
        """
        Patch endpoint to apply given changes to a specific film by film id

        :param film_id: Film id to be changed
        :return: HTTP response with status code
        """
        film_checker = FilmChecker()
        film_data = DBWorker.get_film_by_id(film_id).first()
        patch_data = request.get_json()

        if not film_data:
            return f'Film with {film_id} has not been found. Try again', 400

        film_data = film_data.to_json()

        del film_data['film_id']
        film_data.update(patch_data)
        film_data['release_date'] = film_data['release_date'].strftime(
                '%Y-%m-%d')

        is_correct, errors = film_checker.start_validation(film_data)

        if not is_correct:
            return str(errors), 400

        return f'Changes has been applied to film {film_id}', 200

    @flask_login.login_required
    def delete(self, film_id):
        """
        Delete endpoint to delete given film by id

        :param film_id: Film id to be deleted
        :return: HTTP response with deleted film in json and status code
        """
        film_data = DBWorker.delete_film_by_id(film_id,
                                               flask_login.current_user.user_id)

        if film_data.first():
            return str(film_data.first().to_json()), 200

        return f'Film with id "{film_id}" was not found', 404


@api.route('/director', methods=['GET', 'POST'])
class DirectorEndpoint(Resource):
    """Directors endpoints for GET method"""

    def get(self):
        """
        Get endpoint to get info about present directors, if name or surname is
        not provided retrieve all directors.
        Retrieve directors with partial similarity
        with given name or surname otherwise

        :return: HTTP response with directors list in json and status code
        """
        director_name = request.args.get('name')
        director_surname = request.args.get('surname')

        if director_name is None and director_surname is None:
            return str([director.to_json() for director in
                        DBWorker.get_directors().all()]), 200

        director_query = DBWorker.get_director(director_name, director_surname)

        return str([director.to_json() for director in
                    director_query.all()]), 200
