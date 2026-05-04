"""Payment amount parser — converts English amount words to a numeric value.

Uses a PLY (Python Lex-Yacc) lexer + LALR(1) parser.

Examples
--------
>>> from parser import parse_amount
>>> parse_amount("Two thousand five hundred")
2500.0
>>> parse_amount("one million three hundred forty-two thousand")
1342000.0
>>> parse_amount("1500.00")
1500.0
"""

from __future__ import annotations

from parser.grammar import _PARSE_ERROR, parser
from parser.lexer import lexer


def parse_amount(text: str) -> float | None:
    """Parse *text* into a numeric value.

    Returns ``None`` when the input cannot be interpreted as an amount.
    """
    if not text or not text.strip():
        return None

    _PARSE_ERROR.clear()
    try:
        result = parser.parse(text.strip(), lexer=lexer.clone())
    except Exception:
        return None

    if _PARSE_ERROR:
        return None

    return result
