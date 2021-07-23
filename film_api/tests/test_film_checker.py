import pytest

from film_api.checkers.film_checker import FilmChecker
import film_api.checkers.constrains


@pytest.fixture(name='film_checker')
def fixture_film_checker():
    return FilmChecker()


@pytest.mark.parametrize('film_data', [
    ({'film_title': 'test',
      'release_date': '2020-10-20',
      'rating': 5.23,
      'poster': 'qweqweqweqweqweqwe',
      'created_at': '2021-07-17',
      'producer_id': 2,
      'description': 'description description'
      })
])
def test_film_checker(film_checker, film_data):
    film_checker.check_film_data(film_data)

    print(film_checker.errors)

    assert film_checker.is_correct() is True


@pytest.mark.parametrize('film_data', [
    ({'film_title': 'test',
      'release_date': '2020-10-20',
      'description': 'description description'
      })
])
def test_film_checker_wrong_dict_len(film_checker, film_data):
    assert film_checker.start_validation(film_data) == (
        False, [f'Wrong fields were given. '
                f"Expected ['film_title', 'release_date', 'rating', 'poster', "
                f"'created_at', 'producer_id', 'description'], "
                f'got {film_data.keys()}'])
