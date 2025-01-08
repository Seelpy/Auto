from tokens import *

LETTER_LOWER = '(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)'
LETTER_UPPER = '(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)'
LETTER = f'({LETTER_LOWER}|{LETTER_UPPER})'
DIGIT_NO_ZERO = '(1|2|3|4|5|6|7|8|9)'
DIGIT = f'(0|{DIGIT_NO_ZERO})'
SYMBOL = f'({DIGIT}|{LETTER})'
NUMBER = f'({DIGIT}|{DIGIT_NO_ZERO}{DIGIT}*)'

token_types = [
    Token('BLOCK_COMMENT', f'{{({SYMBOL}| )*}}'),
    Token('LINE_COMMENT', f'//({SYMBOL}| )*'),
    Token('ARRAY', '(A|a)(R|r)(R|r)(A|a)(Y|y)'),
    Token('BEGIN', '(B|b)(E|e)(G|g)(I|i)(N|n)'),
    Token('ELSE', '(E|e)(L|l)(S|s)(E|e)'),
    Token('END', '(E|e)(N|n)(D|d)'),
    Token('IF', '(I|i)(F|f)'),
    Token('OF', '(O|o)(F|f)'),
    Token('OR', '(O|o)(R|r)'),
    Token('PROGRAM', '(P|p)(R|r)(O|o)(G|g)(R|r)(A|a)(M|m)'),
    Token('PROCEDURE', '(P|p)(R|r)(O|o)(C|c)(E|e)(D|d)(U|u)(R|r)(E|e)'),
    Token('THEN', '(T|t)(H|h)(E|e)(N|n)'),
    Token('TYPE', '(T|t)(Y|y)(P|p)(E|e)'),
    Token('VAR', '(V|v)(A|a)(R|r)'),
    Token('MULTIPLICATION', '\\*'),
    Token('PLUS', '\\+'),
    Token('MINUS', '-'),
    Token('DIVIDE', '/'),
    Token('SEMICOLON', ';'),
    Token('COMMA', ','),
    Token('LEFT_PAREN', '\\('),
    Token('RIGHT_PAREN', '\\)'),
    Token('LEFT_BRACKET', '['),
    Token('RIGHT_BRACKET', ']'),
    Token('EQ', '='),
    Token('GREATER', '>'),
    Token('LESS', '<'),
    Token('LESS_EQ', '<='),
    Token('GREATER_EQ', '>='),
    Token('NOT_EQ', '<>'),
    Token('ASSIGN', ':='),
    Token('COLON', ':'),
    Token('DOT', '.'),
    Token('IDENTIFIER', f'({LETTER}|_)({SYMBOL}|_)*'),
    Token('STRING', f'\'{SYMBOL}*\''),
    Token('FLOAT', f'(ε|-){NUMBER}.{DIGIT}+'),
    Token('INTEGER', f'(ε|-){NUMBER}'),
    Token('SPACE', f' |\n|\t|\r'),
    Token('BAD', f'{SYMBOL}'),
]
