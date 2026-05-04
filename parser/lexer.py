"""Lexer for English payment amount words (e.g. "Two thousand five hundred")."""

import ply.lex as lex

# Maps word → integer value; also drives keyword token names.
_ONES = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
    "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
}
_TEENS = {
    "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
}
_TENS = {
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
    "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
}

WORD_VALUES: dict[str, int] = {**_ONES, **_TEENS, **_TENS}

tokens = (
    "ONES", "TEENS", "TENS",
    "HUNDRED", "THOUSAND", "MILLION",
    "AND",
    "FLOAT",
)

literals = ["-"]


def t_FLOAT(t):
    r"\d+(?:\.\d+)?"
    t.value = float(t.value)
    return t


def t_WORD(t):
    r"[a-zA-Z]+"
    word = t.value.lower()
    if word in _ONES:
        t.type = "ONES"
        t.value = _ONES[word]
    elif word in _TEENS:
        t.type = "TEENS"
        t.value = _TEENS[word]
    elif word in _TENS:
        t.type = "TENS"
        t.value = _TENS[word]
    elif word == "hundred":
        t.type = "HUNDRED"
        t.value = 100
    elif word == "thousand":
        t.type = "THOUSAND"
        t.value = 1_000
    elif word == "million":
        t.type = "MILLION"
        t.value = 1_000_000
    elif word == "and":
        t.type = "AND"
        t.value = 0
    else:
        return None  # skip unrecognised words (e.g. "dollars", "UAH")
    return t


t_ignore = " \t\n,"


def t_error(t):
    t.lexer.skip(1)


lexer = lex.lex()
