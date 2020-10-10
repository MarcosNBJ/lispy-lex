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
        ('LBRACE', r'\{'),
        ('RBRACE', r'\}'),
        ('LBRACK', r'\['),
        ('RBRACK', r'\]'),
        ('STRING', r'\"[\w ]*\"'),
        ('COLON', r':'),
        ('COMMA', r','),
        ('NUMBER',   r'\d+(\.\d*)?([eE][+-]?\d+)?'),  # Integer or decimal number
        ('CTE', r'true|false|null'),
        ('NEWLINE',  r'\n'),           # Line endings
        ('SKIP',     r'[ \t]+'),       # Skip over spaces and tabs
        ('MISMATCH', r'.'),            # Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    tokens = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == 'NUMBER':
            value = float(value)
        elif kind == 'ID' and value in keywords:
            kind = value
        elif kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        tokens.append(Token(kind, value))

    return [tokens]

exemplos = [
    """{"nome": "Fabio", "idade": 38, "turmas": ["Compiladores 1", "Fisica para Jogos"]}""",
    """[1, 2.0, 3e4, 5.0e-6, "7",  true, false, null]"""
]

for ex in exemplos:
    print(ex)
    for tok in lex(ex):
        print('    ', tok)
    print()