from flask import Blueprint
from flask_restx import Api

api_parsers_blueprint = Blueprint('api_parsers_blueprint', __name__)
api = Api(api_parsers_blueprint)
film_get_parser = api.parser()

film_get_parser.add_argument('Film id', type=int,
                             help='Film id to be looked (Optional)',
                             location='query')
film_get_parser.add_argument('Film title', type=str,
                             help='Film title, used partial similarity',
                             location='query')
film_get_parser.add_argument('Genre', type=str,
                             help='Film genre, used partial similarity',
                             location='query')
film_get_parser.add_argument('Director name', type=str,
                             help='Director name that filmed the film',
                             location='query')
film_get_parser.add_argument('Director surname', type=str,
                             help='Director surname that filmed the film',
                             location='query')
film_get_parser.add_argument('Release date range', type=str,
                             help='Release date range within which the film '
                                  'was filmed, in next format "YYYY-MM-DD"'
                                  ' separated by comma',
                             location='query')
film_get_parser.add_argument('Sort by dates', type=int,
                             help='Flag to sort films by dates, '
                                  '-1 for descending, 0 for no sort,'
                                  ' 1 for ascending',
                             location='query')
film_get_parser.add_argument('Sort by rating', type=int,
                             help='Flag to sort films by rating, '
                                  '-1 for descending, 0 for no sort,'
                                  ' 1 for ascending',
                             location='query')

film_post_parser = api.parser()

film_post_parser.add_argument('Film title', type=str,
                              help='Film title',
                              location='json')
film_post_parser.add_argument('Release date', type=str,
                              help='Release date in next format "YYYY-MM-DD"',
                              location='json')
film_post_parser.add_argument('Poster', type=str,
                              help='Flag to sort films by dates, '
                                   '-1 for descending, 0 for no sort,'
                                   ' 1 for ascending',
                              location='json')
film_post_parser.add_argument('Created by', type=int,
                              help='Flag to sort films by dates, '
                                   '-1 for descending, 0 for no sort,'
                                   ' 1 for ascending',
                              location='json')
film_post_parser.add_argument('Director id', type=int,
                              help='Flag to sort films by dates, '
                                   '-1 for descending, 0 for no sort,'
                                   ' 1 for ascending',
                              location='json')
film_post_parser.add_argument('Description', type=str,
                              help='Flag to sort films by dates, '
                                   '-1 for descending, 0 for no sort,'
                                   ' 1 for ascending',
                              location='json')
film_post_parser.add_argument('Rating', type=float,
                              help='Flag to sort films by dates, '
                                   '-1 for descending, 0 for no sort,'
                                   ' 1 for ascending',
                              location='json')

directors_get_parser = api.parser()

directors_get_parser.add_argument('Name', type=str,
                                  help='Name of the director,'
                                       ' partial similarity',
                                  location='query')
directors_get_parser.add_argument('Surname', type=str,
                                  help='Surname of the director,'
                                       ' partial similarity',
                                  location='query')
