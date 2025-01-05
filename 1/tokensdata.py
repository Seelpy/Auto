from tokens import *

ALL_DIGITS = "1|2|3|4|5|6|7|8|9|0"
NOT_NULL_DIGITS = "1|2|3|4|5|6|7|8|9"
ALL_ALF_LOWERCASE = "a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z"
ALL_ALF_UPPERCASE = "A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z"
ALL_ALF = ALL_ALF_LOWERCASE + "|" + ALL_ALF_UPPERCASE
ALL_SYM = ALL_ALF + "|" + ALL_DIGITS
ALL_SPEC_SYM = " "
ALL_SYM_WITH_SPEC = ALL_ALF + "|" + ALL_DIGITS + "|" + ALL_SPEC_SYM

KWORD_TOKEN = "KWORD"
SEPARATE_TOKEN = "SEP"
ID_TOKEN = "ID"
DOT_TOKEN = "DOT"
ASSIGN_TOKEN = "ASSIGN"
TYPE_TOKEN = "TYPE"
FUNC_TOKEN = "FUNC"
LITERAL_TOKEN = "LITERAL"
INTEGER_TOKEN = "INT"
BOOL_TOKEN = "BOOL"
FLOT_TOKEN = "FLOAT"
COMMENT_TOKEN = "COMMENT"

tokens = [
    Token(KWORD_TOKEN, "VAR|BEGIN|END"),
    Token(COMMENT_TOKEN, "(///)" + f"({ALL_SYM_WITH_SPEC})*" + "(///)"),
    Token(FUNC_TOKEN, "WRITE|READ|READLN|WRITELN"),
    Token(TYPE_TOKEN, "BOOL|STR|TEXT|FLOAT|INTEGER"),
    Token(LITERAL_TOKEN,  "'" + "(" + ALL_SYM + ")" + "*" + "'"),
    Token(INTEGER_TOKEN, "(" + ALL_DIGITS + ")" + "|" + "(" + "(" + NOT_NULL_DIGITS + ")" + "(" + ALL_DIGITS + ")" + "+" + ")"),
    Token(BOOL_TOKEN, "TRUE|true|True|FALSE|False|false"),
    Token(SEPARATE_TOKEN, "&"),
    Token(ID_TOKEN, "(" + ALL_ALF_LOWERCASE + ")" + "(" + ALL_SYM + ")" + "*"),
    Token(DOT_TOKEN, "."),
    Token(ASSIGN_TOKEN, ":="),
    Token(FLOT_TOKEN, f"((({ALL_DIGITS})+).(({ALL_DIGITS})+))|(.({ALL_DIGITS})+)"),
]

tokensMap = {token.id: token for token in tokens}

SpaceToken = EmptyToken(" ")
TabToken = EmptyToken("(    )")
SpacesToken = EmptyToken("( )*")

VarToken = ConcreteToken(tokensMap[KWORD_TOKEN], "VAR")
BeginToken = ConcreteToken(tokensMap[KWORD_TOKEN], "BEGIN")
EndToken = ConcreteToken(tokensMap[KWORD_TOKEN], "END")
DotToken = tokensMap[DOT_TOKEN]
TypeToken = tokensMap[TYPE_TOKEN]
IDToken = tokensMap[ID_TOKEN]
IntegerToken = tokensMap[INTEGER_TOKEN]
BoolToken = tokensMap[BOOL_TOKEN]
AssignToken = tokensMap[ASSIGN_TOKEN]
LiteralToken = tokensMap[LITERAL_TOKEN]
EndLineToken = ConcreteToken(tokensMap[SEPARATE_TOKEN], "&")
CommentToken = tokensMap[COMMENT_TOKEN]
FloatToken = tokensMap[FLOT_TOKEN]
