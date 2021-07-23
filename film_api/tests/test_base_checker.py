import pytest

from decimal import Decimal

from film_api.checkers.base_checker import BaseChecker


@pytest.fixture(name='base_checker')
def fixture_base_checker():
    return BaseChecker()


@pytest.mark.parametrize('string, max_length', [
    ('test', 4),
    ('quadros', 10),
    ('s' * 99, 100)
])
def test_check_varchar(base_checker, string, max_length):
    base_checker.check_varchar(string, max_length)

    print(base_checker.errors)

    assert base_checker.is_correct()
    assert len(base_checker.errors) == 0


@pytest.mark.parametrize('data, max_length', [
    (2, 10),
    (2.0, 10),
    (True, 10),
    ({'1': 2}, 10),
])
def test_check_varchar_wrong_type(base_checker, data, max_length):
    base_checker.check_varchar(data, max_length)

    assert base_checker.is_correct() is False
    assert base_checker.errors[0] == \
           f'Wrong type, expected {str}, got {type(data)}'


@pytest.mark.parametrize('data, max_length', [
    ('e' * 5, 4),
    ('e' * 5, 0),
    ('e' * 11, 10),
])
def test_check_varchar_wrong_length(base_checker, data, max_length):
    base_checker.check_varchar(data, max_length)

    assert base_checker.is_correct() is False
    assert base_checker.errors[0] == \
           f'Expected max length of {max_length}, got {len(data)}'


@pytest.mark.parametrize('num, min_v, max_v', [
    (50, 5, 200),
    (5, 5, 10),
    (5.2, 5, 6),
    (5.2, 5.2, 6),
    (6., 5.2, 6.01),
    (Decimal(6.), 5.2, 6.01),
])
def test_check_number(base_checker, num, min_v, max_v):
    base_checker.check_number(num, min_v, max_v)

    assert base_checker.is_correct() is True
    assert len(base_checker.errors) == 0


@pytest.mark.parametrize('num, min_v, max_v', [
    ('er', 1, 2),
    (('er', 2), 1, 2),
    (['er', 2], 1, 2),
])
def test_check_number_wrong_type(base_checker, num, min_v, max_v):
    base_checker.check_number(num, min_v, max_v)

    assert base_checker.is_correct() is False
    assert len(base_checker.errors) == 1


@pytest.mark.parametrize('num, min_v, max_v', [
    (5, 6, 10),
    (10, 6, 10),
    (6.001, 6.01, 10.2),
    (10.21, 6.01, 10.2),
    (Decimal(6), Decimal(7), Decimal(8)),
    (Decimal(5.9), Decimal(6), Decimal(7)),
    (Decimal(8), Decimal(6), Decimal(8)),
    (Decimal(7.1), Decimal(6), Decimal(7)),
])
def test_check_number_out_of_range(base_checker, num, min_v, max_v):
    base_checker.check_number(num, min_v, max_v)

    assert base_checker.is_correct() is False
    assert len(base_checker.errors) == 1


@pytest.mark.parametrize('date', [
    '1888-11-21',
    '2012-10-21',
    '1900-12-31',
    '2021-01-01',
])
def test_check_date(base_checker, date):
    base_checker.check_date(date)

    assert base_checker.is_correct() is True
    assert len(base_checker.errors) == 0


@pytest.mark.parametrize('date', [
    '11-21-1990',
    '1998.10.20',
    '1998/10/20',
    'asdasd',
])
def test_check_date_wrong_forms(base_checker, date):
    base_checker.check_date(date)

    assert base_checker.is_correct() is False
    assert base_checker.errors[0] == \
           f'Wrong date format. Expected "YYYY-MM-DD" format, got {date}'


@pytest.mark.parametrize('date, expected', [
    ('1800-1-1', 'Wrong year. First film was filmed in 1888. Got 1800'),
    ('2022-1-1', 'Wrong year. First film was filmed in 1888. Got 2022'),
    ('1900-0-1', 'Wrong month. Got 0'),
    ('1900-13-1', 'Wrong month. Got 13'),
    ('1900-1-0', 'Wrong day. Got 0'),
    ('1900-1-32', 'Wrong day. Got 32'),
])
def test_check_date_out_of_range(base_checker, date, expected):
    base_checker.check_date(date)

    assert base_checker.is_correct() is False
    assert base_checker.errors[0] == expected
