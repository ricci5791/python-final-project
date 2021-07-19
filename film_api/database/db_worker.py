"""Module that contains basic database queries"""
from typing import Optional

from sqlalchemy.orm import Query

from film_api.database import models


class DBWorker:
    """Proxy class for retrieving data from the database"""

    @staticmethod
    def get_user_by_id(user_id) -> Optional[models.User]:
        """
        Retrieve user from db by user_id

        :param user_id:
        :return: User instance if such exists
        """
        return models.User.query.filter_by(user_id=user_id).first()

    @staticmethod
    def get_user_by_creds(username, password) -> Optional[models.User]:
        """
        Retrieve user from db by username and password

        :param username: Username of user
        :param password: Password of user
        :return: User instance if such exists
        """
        return models.User.query.filter_by(username=username).filter_by(
                password=password).first()

    @staticmethod
    def get_user_by_api_key(api_key) -> Optional[models.User]:
        """
        Retrieve user from db by api_key

        :param api_key:
        :return: User instance if such exists
        :rtype: User
        """
        return models.User.query.filter_by(api_key=api_key).first()

    @staticmethod
    def get_film_by_id(film_id) -> Query:
        """
        Retrieve film by it's id

        :param film_id: Id of the film
        :return: Query of film if found
        :rtype: Query
        """
        return models.Film.query.filter_by(film_id=film_id)

    @staticmethod
    def get_film_by_id_by_user(film_id, user_id) -> Query:
        """
        Retrieve film that s created by some user

        :param film_id: Film id to be searched
        :param user_id: User id that created film instance
        :return: Query of film that has been found
        :rtype: Query
        """""
        return models.Film.query.filter_by(film_id=film_id) \
            .filter_by(created_by=user_id)

    @staticmethod
    def delete_film_by_id(film_id, user_id) -> Query:
        """
        Delete film by id and commit changes to the database

        :param film_id: Film id to be deleted
        :param user_id: User that intent to delete the film
        :return: Query of film
        :rtype: Query
        """
        film = DBWorker.get_film_by_id(film_id)

        models.Film.query.filter_by(film_id=film_id) \
            .filter_by(created_by=user_id).delete()

        models.db_session.commit()

        if film:
            return film
        return None

    @staticmethod
    def get_film_by_title(film_title: str) -> Query:
        """
        Search for films with partial similarity with given title

        :param film_title: Title to be searched
        :return: Query of films which title has matched
        :rtype: Query
        """
        search = "%{}%".format(film_title)
        return models.Film.query.filter(models.Film.film_title.ilike(search))

    @staticmethod
    def filter_film_by_genre(film_query: Query, genre: str) -> Query:
        """
        Retrieve films with given genre

        :param film_query: Created query of films to be filtered by genre
        :param genre: Genre to be filtered by
        :return: Filtered query of films
        :rtype: Query
        """
        film_query = film_query.join(models.FilmGenre,
                                     models.Film.film_id ==
                                     models.FilmGenre.film_id) \
            .join(models.Genres,
                  models.FilmGenre.genre_id == models.Genres.genre_id) \
            .where(models.Genres.genre_name == genre) \
            .group_by(models.Film.film_id)

        return film_query

    @staticmethod
    def filter_film_by_release_date(film_query: Query, start_date: str,
                                    end_date: str) -> Query:
        """
        Filter film query that within given date range

        :param film_query: Query to be filtered
        :param start_date: From filter date
        :param end_date: To filter date
        :return: Filtered query by date
        :rtype: Query
        """
        film_query = film_query.filter(models.Film.release_date.
                                       between(start_date, end_date))

        return film_query

    @staticmethod
    def sort_film(film_query: Query, dates: int, rating: int) -> Query:
        """
        Sort film query by dates or rating

        :param film_query: Query to be sorted
        :param dates: -1 for descending sort,0 for no sort, 1 for ascending sort
        :param rating: -1 for descending sort,0 for no sort,1 for ascending sort
        :return: Sorted query of films
        :rtype: Query
        """
        if dates != 0:
            if dates == -1:
                print('get here!')
                film_query = film_query.order_by(
                        models.Film.release_date.desc())
            elif dates == 1:
                film_query = film_query.order_by(models.Film.release_date.asc())

        if rating != 0:
            if rating == -1:
                film_query = film_query.order_by(models.Film.rating.desc())
            elif rating == 1:
                film_query = film_query.order_by(models.Film.rating.asc())

        return film_query

    @staticmethod
    def filter_film_by_director(film_query, director_name: str = None,
                                director_surname: str = None) -> Query:
        """
        Filter film query by director name or surname (by exact similarity)

        :param film_query: Query of films to be filtered
        :param director_name: Director name
        :param director_surname: Director surname
        :return: Query of films with given director
        :rtype: Query
        """
        if director_name is not None or director_surname is not None:
            film_query = film_query.join(models.Director,
                                         models.Film.director_id ==
                                         models.Director.director_id)
        if director_name:
            film_query = film_query.filter_by(name=director_name)
        if director_surname:
            film_query = film_query.filter_by(surname=director_surname)

        return film_query

    @staticmethod
    def get_directors() -> Query:
        """
        Retrieve all directors from the database

        :return: Query of directors
        :rtype: Query
        """
        return models.Director.query

    @staticmethod
    def get_director(director_name=None, director_surname=None):
        """
        Retrieve directors with partial similarity with given name or surname

        :param director_name: Director name
        :param director_surname: Director surname
        :return: Query of directors that was found
        :rtype: Query
        """
        directors_query = models.Director.query

        if director_name:
            name_search = "%{}%".format(director_name)
            directors_query = directors_query.filter(
                    models.Director.name.ilike(name_search))

        if director_surname:
            surname_search = "%{}%".format(director_surname)
            directors_query = directors_query.filter(
                    models.Director.surname.ilike(surname_search))

        return directors_query
