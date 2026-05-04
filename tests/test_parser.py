import pytest
from parser import parse_amount


@pytest.mark.parametrize("text,expected", [
    ("zero", 0.0),
    ("one", 1.0),
    ("nineteen", 19.0),
    ("twenty", 20.0),
    ("twenty-one", 21.0),
    ("twenty one", 21.0),
    ("ninety-nine", 99.0),
    ("one hundred", 100.0),
    ("one hundred and five", 105.0),
    ("three hundred forty-two", 342.0),
    ("one thousand", 1000.0),
    ("two thousand five hundred", 2500.0),
    ("one million", 1_000_000.0),
    ("one million three hundred forty-two thousand", 1_342_000.0),
    ("two million five hundred thousand three hundred twenty-one", 2_500_321.0),
    # Raw numeric strings pass through as-is
    ("1500.00", 1500.0),
    ("42", 42.0),
    # Extra words (currency names) are ignored by the lexer
    ("one thousand dollars", 1000.0),
    ("five hundred UAH", 500.0),
])
def test_parse_amount(text, expected):
    assert parse_amount(text) == pytest.approx(expected)


def test_empty_returns_none():
    assert parse_amount("") is None


def test_whitespace_returns_none():
    assert parse_amount("   ") is None


def test_garbage_returns_none():
    assert parse_amount("not a number at all xyz") is None
