from tokens import *

BIG_SYM = "(0|1|2|3|4|5|6|7|8|9|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|!|\"|#|$|%|&|'|\\(|\\)|\*|\+|,|-|.|/|:|;|<|=|>|?|@|[|]|^|_|`|{|\\||}|~| |\t|\r)"
BIG_SYM_WITHOUT = "(0|1|2|3|4|5|6|7|8|9|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|!|\"|#|$|%|&|\\(|\\)|\*|\+|,|-|.|/|:|;|<|=|>|?|@|[|]|^|_|`|{|\\||}|~| |\t|\r)"
LETTER_LOWER = '(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)'
LETTER_UPPER = '(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)'
LETTER = f'({LETTER_LOWER}|{LETTER_UPPER})'
DIGIT_NO_ZERO = '(1|2|3|4|5|6|7|8|9)'
DIGIT = f'(0|{DIGIT_NO_ZERO})'
SYMBOL = f'({DIGIT}|{LETTER})'
NUMBER = f'({DIGIT}|{DIGIT_NO_ZERO}{DIGIT}*)'
E_POSITIV = f'((e|E){DIGIT}+)|((e|E)\\+{DIGIT}+)'
E_NEGATIV = f'((e|E)-{DIGIT}+)'

SEPARATOR = ",.:;*/+-()[]=<>\n\r\t "

token_types = [
    Token('BLOCK_COMMENT', f'{{({BIG_SYM}| )*}}', isSeparate=True, needMiss=True),
    Token('LINE_COMMENT', f'//({BIG_SYM}| )*', isSeparate=True, needMiss=True),
    Token('ARRAY', '(A|a)(R|r)(R|r)(A|a)(Y|y)', needAfterSeparate=True),
    Token('BEGIN', '(B|b)(E|e)(G|g)(I|i)(N|n)', needAfterSeparate=True),
    Token('ELSE', '(E|e)(L|l)(S|s)(E|e)', needAfterSeparate=True),
    Token('END', '(E|e)(N|n)(D|d)', needAfterSeparate=True),
    Token('IF', '(I|i)(F|f)', needAfterSeparate=True),
    Token('OF', '(O|o)(F|f)', needAfterSeparate=True),
    Token('OR', '(O|o)(R|r)', needAfterSeparate=True),
    Token('PROGRAM', '(P|p)(R|r)(O|o)(G|g)(R|r)(A|a)(M|m)', needAfterSeparate=True),
    Token('PROCEDURE', '(P|p)(R|r)(O|o)(C|c)(E|e)(D|d)(U|u)(R|r)(E|e)'),
    Token('THEN', '(T|t)(H|h)(E|e)(N|n)', needAfterSeparate=True),
    Token('TYPE', '(T|t)(Y|y)(P|p)(E|e)', needAfterSeparate=True),
    Token('VAR', '(V|v)(A|a)(R|r)', needAfterSeparate=True),
    Token('MULTIPLICATION', '\\*', isSeparate=True),
    Token('PLUS', '\\+', isSeparate=True),
    Token('MINUS', '-', isSeparate=True),
    Token('DIVIDE', '/', isSeparate=True),
    Token('SEMICOLON', ';', isSeparate=True),
    Token('COMMA', ',', isSeparate=True),
    Token('LEFT_PAREN', '\\(', isSeparate=True),
    Token('RIGHT_PAREN', '\\)', isSeparate=True),
    Token('LEFT_BRACKET', '[', isSeparate=True),
    Token('RIGHT_BRACKET', ']', isSeparate=True),
    Token('EQ', '=', isSeparate=True),
    Token('NOT_EQ', '<>', isSeparate=True),
    Token('LESS_EQ', '<=', isSeparate=True),
    Token('GREATER_EQ', '>=', isSeparate=True),
    Token('GREATER', '>', isSeparate=True),
    Token('LESS', '<', isSeparate=True),
    Token('ASSIGN', ':=', isSeparate=True),
    Token('COLON', ':', isSeparate=True),
    Token('DOT', '.', isSeparate=True),
    Token('IDENTIFIER', f'({LETTER}|_)({SYMBOL}|_)*', maxLen=256, needAfterSeparate=True),
    Token('STRING', f'\'{BIG_SYM_WITHOUT}*\'', needAfterSeparate=True),
    Token('FLOAT', f'((ε|-){NUMBER}.{DIGIT}+({E_POSITIV}|{E_NEGATIV}|ε))|((ε|-){NUMBER}({E_NEGATIV}))', needAfterSeparate=True),
    Token('INTEGER', f'(ε|-){NUMBER}({E_POSITIV}|ε)', maxLen=16, needAfterSeparate=True),
    Token('SPACE', f' |\n|\t|\r', isSeparate=True, needMiss=True),
]

# TODO проверка на длину идентификаторы +++++
# TODO комментарий нужно сбрасывать +++++
# TODO 1a - error ++++++
# TODO e -  ++++++
# TODO 123a123 - ошибка
# TODO <> - неравно добавить   ++++
# TODO a.b - тоже нужно ь ++++
# TODO стаистика по встреченным идентификаторам