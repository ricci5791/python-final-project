"""Module with length and other constraints for database models"""

film_constraint_dict = {'film_title': 100, 'poster': 1_000_000,
                        'description': 1_000_000_000}

FILM_RATING_MIN = 0.1
FILM_RATING_MAX = 10.0
