import re
from typing import NamedTuple, Iterable


class Token(NamedTuple):
    kind: str
    value: str


def lex(code: str) -> Iterable[Token]:
    """
    Retorna sequência de objetos do tipo token correspondendo à análise léxica
    da string de código fornecida.
    """
    keywords = {'IF', 'THEN', 'ENDIF', 'FOR', 'NEXT', 'GOSUB', 'RETURN'}
    token_specification = [
        ('LPAR', r'\('),
        ('RPAR', r'\)'),
        ('CHAR', r'#\\[^ ]*'), 
        ('NUMBER', r'[+-]?(\d+(\.\d+)?)'), 
        ('NAME', r'([a-zA-Z_!?%$@<>\'^~&$:=\/*.][-\w+*\/!?%$@<>\'^~&$:=\/*.]*)|([+-])'),
        ('BOOL', r'#[t|f]+'),
        ('STRING', r'"(?:[^"\\]|\\.)*"'),
        ('COMMENT', r';[^\n]*'),
        ('SKIP',     r'[ \t]+'),       # Skip over spaces and tabs
        ('MISMATCH', r'.'),            # Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    tokens = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()

        if kind == 'SKIP' or kind == 'COMMENT':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        tokens.append(Token(kind, value))

    return tokens