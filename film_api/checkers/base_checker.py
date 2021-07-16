"""Module with base checker class"""
import datetime
from typing import List
from decimal import Decimal

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
        if isinstance(str, data):
            self.mark_incorrect()
            self._add_error_wrong_type(str, type(data))

        if len(data) > max_length:
            self.mark_incorrect()
            self.errors.append(
                    f'Expected max length of {max_length}, got {len(data)}')

    def check_number(self, data, min_value: Numeric = None,
                     max_value: Numeric = None) -> None:
        """
        Checks number fields to be within the given range

        :param data: Number to be checked
        :param min_value: Min range number
        :param max_value: Max range number

        :return: None
        """
        if type(data) not in Numeric:
            self.mark_incorrect()
            self._add_error_wrong_type(Numeric, type(data))

        if data > min_value or data > max_value:
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
        split_date = data.split('-')

        if len(split_date) != 3:
            self.mark_incorrect()
            self.errors.append(
                    f'Wrong date format. Expected "YYYY-MM-DD" format, '
                    f'got {data}')

        if not 1888 < int(split_date[0]) < datetime.datetime.now().year:
            self.mark_incorrect()
            self.errors.append(f'Wrong year. First film was filmed in 1888. '
                               f'Got {split_date[0]}')

        if not 0 < int(split_date[1]) < 13:
            self.mark_incorrect()
            self.errors.append(f'Wrong month. Got {split_date[1]}')

        if not 0 < int(split_date[2]) < 31:
            self.mark_incorrect()
            self.errors.append(f'Wrong day. Got {split_date[2]}')

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
