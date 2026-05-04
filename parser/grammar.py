"""YACC grammar for English payment amount words.

Grammar (simplified BNF):

    start       : expr
    expr        : FLOAT
                | number_words
    number_words: millions | thousands | hundreds | sub_hundred
    millions    : number_words MILLION
                | number_words MILLION number_words
    thousands   : number_words THOUSAND
                | number_words THOUSAND number_words
    hundreds    : sub_hundred HUNDRED
                | sub_hundred HUNDRED AND sub_hundred
                | sub_hundred HUNDRED sub_hundred
    sub_hundred : TENS
                | ONES
                | TEENS
                | TENS '-' ONES
                | TENS ONES
"""

import ply.yacc as yacc

from parser.lexer import tokens  # noqa: F401 — yacc requires tokens in scope

_PARSE_ERROR: list[str] = []


def p_start(p):
    "start : expr"
    p[0] = p[1]


def p_expr_float(p):
    "expr : FLOAT"
    p[0] = p[1]


def p_expr_words(p):
    "expr : number_words"
    p[0] = float(p[1])


# ── millions ──────────────────────────────────────────────────────────────────

def p_millions_simple(p):
    "number_words : number_words MILLION"
    p[0] = p[1] * p[2]


def p_millions_with_rest(p):
    "number_words : number_words MILLION number_words"
    p[0] = p[1] * p[2] + p[3]


# ── thousands ─────────────────────────────────────────────────────────────────

def p_thousands_simple(p):
    "number_words : number_words THOUSAND"
    p[0] = p[1] * p[2]


def p_thousands_with_rest(p):
    "number_words : number_words THOUSAND number_words"
    p[0] = p[1] * p[2] + p[3]


# ── hundreds ──────────────────────────────────────────────────────────────────

def p_hundreds_simple(p):
    "number_words : sub_hundred HUNDRED"
    p[0] = p[1] * p[2]


def p_hundreds_and(p):
    "number_words : sub_hundred HUNDRED AND sub_hundred"
    p[0] = p[1] * p[2] + p[4]


def p_hundreds_with_rest(p):
    "number_words : sub_hundred HUNDRED sub_hundred"
    p[0] = p[1] * p[2] + p[3]


# ── sub-hundred values (< 100) ────────────────────────────────────────────────

def p_sub_hundreds_base(p):
    """sub_hundred : TENS
                   | ONES
                   | TEENS"""
    p[0] = p[1]


def p_sub_hundred_hyphen(p):
    "sub_hundred : TENS '-' ONES"
    p[0] = p[1] + p[3]


def p_sub_hundred_space(p):
    "sub_hundred : TENS ONES"
    p[0] = p[1] + p[2]


# ── number_words from sub_hundred ────────────────────────────────────────────

def p_number_words_sub(p):
    "number_words : sub_hundred"
    p[0] = p[1]


# ── error ─────────────────────────────────────────────────────────────────────

def p_error(p):
    if p:
        _PARSE_ERROR.append(f"Unexpected token '{p.value}' at position {p.lexpos}")


parser = yacc.yacc(debug=False, write_tables=False, errorlog=yacc.NullLogger())
