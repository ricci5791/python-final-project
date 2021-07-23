from flask import Blueprint
from flask_restx import Api

api_parsers_blueprint = Blueprint('api_parsers_blueprint', __name__)
api = Api(api_parsers_blueprint)
film_get_parser = api.parser()

film_get_parser.add_argument('Film id', type=int,
                             help='Film id to be looked (Optional)',
                             location='query')
film_get_parser.add_argument('title', type=str,
                             help='Film title, used partial similarity',
                             location='query')
film_get_parser.add_argument('genre', type=str,
                             help='Film genre, used partial similarity',
                             location='query')
film_get_parser.add_argument('director_name', type=str,
                             help='Director name that filmed the film',
                             location='query')
film_get_parser.add_argument('director_surname', type=str,
                             help='Director surname that filmed the film',
                             location='query')
film_get_parser.add_argument('release_date', type=str,
                             help='Release date range within which the film '
                                  'was filmed, in next format "YYYY-MM-DD"'
                                  ' separated by comma',
                             location='query')
film_get_parser.add_argument('sort_dates', type=int,
                             help='Flag to sort films by dates, '
                                  '-1 for descending, 0 for no sort,'
                                  ' 1 for ascending',
                             location='query')
film_get_parser.add_argument('sort_rating', type=int,
                             help='Flag to sort films by rating, '
                                  '-1 for descending, 0 for no sort,'
                                  ' 1 for ascending',
                             location='query')
film_get_parser.add_argument('page', type=int,
                             help='Page number for pagination',
                             location='query')

film_post_parser = api.parser()

film_post_parser.add_argument('film_title', type=str,
                              help='Film title',
                              location='json')
film_post_parser.add_argument('release_date', type=str,
                              help='Release date in next format "YYYY-MM-DD"',
                              location='json')
film_post_parser.add_argument('poster', type=str,
                              help='Flag to sort films by dates, '
                                   '-1 for descending, 0 for no sort,'
                                   ' 1 for ascending',
                              location='json')
film_post_parser.add_argument('created_by', type=int,
                              help='Flag to sort films by dates, '
                                   '-1 for descending, 0 for no sort,'
                                   ' 1 for ascending',
                              location='json')
film_post_parser.add_argument('director_id', type=int,
                              help='Flag to sort films by dates, '
                                   '-1 for descending, 0 for no sort,'
                                   ' 1 for ascending',
                              location='json')
film_post_parser.add_argument('description', type=str,
                              help='Flag to sort films by dates, '
                                   '-1 for descending, 0 for no sort,'
                                   ' 1 for ascending',
                              location='json')
film_post_parser.add_argument('rating', type=float,
                              help='Flag to sort films by dates, '
                                   '-1 for descending, 0 for no sort,'
                                   ' 1 for ascending',
                              location='json')

directors_get_parser = api.parser()

directors_get_parser.add_argument('name', type=str,
                                  help='Name of the director,'
                                       ' partial similarity',
                                  location='query')
directors_get_parser.add_argument('surname', type=str,
                                  help='Surname of the director,'
                                       ' partial similarity',
                                  location='query')
directors_get_parser.add_argument('page', type=int,
                                  help='Page number for pagination',
                                  location='query')
