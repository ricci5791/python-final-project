"""Module with base checker class"""
import datetime
from typing import List
from decimal import Decimal
import re

Numeric = [int, float, Decimal]


class BaseChecker:
    """
    Base class for checkers for further implementation
    """

    def __init__(self):
        self._is_correct: bool = True
        self.errors: List[str] = []

    def _add_error_wrong_type(self, expected_type, wrong_type):
        self.errors.append(
                f'Wrong type, expected {expected_type}, got {wrong_type}')

    def check_varchar(self, data, max_length: int) -> None:
        """
        Checks varchar for length and type to be string

        :param data: String to be checked
        :param max_length: Max length

        :return: None
        """
        if not isinstance(data, str):
            self.mark_incorrect()
            self._add_error_wrong_type(str, type(data))
            return

        if len(data) > max_length:
            self.mark_incorrect()
            self.errors.append(
                    f'Expected max length of {max_length}, got {len(data)}')

    def check_number(self, data, min_value: Numeric,
                     max_value: Numeric) -> None:
        """
        Checks number fields to be within the given range

        :param data: Number to be checked
        :param min_value: Min range number (included)
        :param max_value: Max range number (excluded)

        :return: None
        """
        if type(data) not in Numeric:
            self.mark_incorrect()
            self._add_error_wrong_type(Numeric, type(data))
            return

        if not min_value <= data < max_value:
            self.mark_incorrect()
            self.errors.append(
                    f'Value out of range. Expected from {min_value} to'
                    f' {max_value}. Got {data} instead')

    def check_date(self, data: str) -> None:
        """
        Check film release date for correctness

        :param data: String that contains date of format 'YYYY-MM-DD'
        :return: None
        """
        if not isinstance(data, str):
            self.mark_incorrect()
            self._add_error_wrong_type(str, type(data))
            return

        if not re.match(r'\d{4}-\d{1,2}-\d{1,2}', data):
            self.mark_incorrect()
            self.errors.append(
                    f'Wrong date format. Expected "YYYY-MM-DD" format, '
                    f'got {data}')
            return

        year, month, day = [int(x) for x in data.split('-')]

        if not 1888 <= year <= datetime.datetime.now().year:
            self.mark_incorrect()
            self.errors.append(f'Wrong year. First film was filmed in 1888. '
                               f'Got {year}')

        if not 0 < month < 13:
            self.mark_incorrect()
            self.errors.append(f'Wrong month. Got {month}')

        if not 0 < day < 32:
            self.mark_incorrect()
            self.errors.append(f'Wrong day. Got {day}')

    def mark_incorrect(self) -> None:
        """
        Set checker state of valid data to be False

        :return: None
        """
        self._is_correct = False

    def is_correct(self) -> bool:
        """
        Return state of checker

        :return: True if data validation is complete
        :rtype: bool
        """
        return self._is_correct

    def get_errors(self) -> List[str]:
        """
        Return all errors that occurred during the validation

        :return: List of errors
        :rtype: List[str]
        """
        return self.errors

    def __iter__(self):
        return iter(self.errors)
