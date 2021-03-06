"""Module with film checker class"""
from typing import Dict, Optional, List, Tuple

import film_api.checkers.constrains as constr
from film_api.checkers.base_checker import BaseChecker


class FilmChecker(BaseChecker):
    """
    Film checker class with validation methods
    """
    film_reference_list = ['created_by', 'description', 'director_id',
                           'film_title', 'poster', 'rating', 'release_date']

    film_str_data = ['film_title', 'poster', 'description']
    film_date_data = ['release_date']
    film_numeric_data = ['rating']

    def check_film_data(self, film_data: Dict) -> None:
        """
        Checks film data that is given for basic column type restrictions

        :param film_data: Dict of film data
        :return: None
        """
        if sorted(list(film_data.keys())) != self.film_reference_list:
            self.mark_incorrect()
            self.errors.append(f'Wrong fields were given. '
                               f'Expected {self.film_reference_list}, '
                               f'got {film_data.keys()}')
            return

        for key in self.film_str_data:
            self.check_varchar(film_data[key],
                               constr.film_constraint_dict[key])

        for key in self.film_date_data:
            self.check_date(film_data[key])

        for key in self.film_numeric_data:
            self.check_number(film_data[key],
                              constr.FILM_RATING_MIN,
                              constr.FILM_RATING_MAX)

    def start_validation(self, film_data: Dict) \
            -> Tuple[bool, Optional[List[str]]]:
        """
        Perform validation of film data and returns result of it

        :param film_data: Dict that contains film data
        :return: Correctness flag and errors that occurred during the check
        :rtype: Tuple[bool, Optional[List]]
        """
        self.check_film_data(film_data)

        return self.is_correct(), self.get_errors()
