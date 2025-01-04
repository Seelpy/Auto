from __future__ import annotations

from abc import ABC, abstractmethod
import regtodka


class RegularInterface(ABC):
    @abstractmethod
    def process(self, string: str, start: int) -> [str, str, int | None]:
        pass

class Token(RegularInterface):
    def __init__(self, id: str, reg: str):
        self.id = id
        self.reg = reg
        self.slider = regtodka.RegToDKAConverter().convert(reg)

    def process(self, string: str, start: int) -> [str, str, int | None]:
        i = start
        for c in string[start:]:
            if self.slider.IsFinal():
                break
            try:
                self.slider.Move(c)
            except:
                if self.slider.IsPossibleFinish():
                    return self.id, string[start: i], None
                return "", "", i
            i += 1
        self.reset()
        return self.id, string[start: i], None

    def reset(self):
        self.slider.Reset()


class EmptyToken(RegularInterface):
    def __init__(self, reg: str):
        self.token = Token("", reg)

    def process(self, string: str, start: int) -> [str, str, int | None]:
        return self.token.process(string, start)

class ConcreteToken(RegularInterface):
    def __init__(self, token: Token, value: str):
        self.token = token
        self.value = value

    def process(self, string: str, start: int) -> [str, str, int | None]:
        token, val, errIndx = self.token.process(string, start)
        if errIndx != None:
            return token, val, errIndx
        if val != self.value:
            return token, "", start
        return token, val, None


ALL_DIGITS = "1|2|3|4|5|6|7|8|9|0"
NOT_NULL_DIGITS = "1|2|3|4|5|6|7|8|9"
ALL_ALF_LOWERCASE = "a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z"
ALL_ALF_UPPERCASE = "A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z"
ALL_ALF = ALL_ALF_LOWERCASE + "|" + ALL_ALF_UPPERCASE
ALL_SYM = ALL_ALF + "|" + ALL_DIGITS

KWORD_TOKEN = "KWORD"
SEPARATE_TOKEN = "SEP"
ID_TOKEN = "ID"
DOT_TOKEN = "DOT"
ASSIGN_TOKEN = "ASSIGN"
TYPE_TOKEN = "TYPE"
FUNC_TOKEN = "FUNC"
LITERAL_TOKEN = "LITERAL"
INEGER_TOKEN = "INT"
BOOL_TOKEN = "BOOL"

tokens = [
    Token(KWORD_TOKEN, "VAR|BEGIN|END|WRITE|READ"),
    Token(FUNC_TOKEN, "WRITE|READ|READLN|WRITELN"),
    Token(TYPE_TOKEN, "BOOL|STR|TEXT|FLOAT|INTEGER"),
    Token(LITERAL_TOKEN,  "'" + "(" + ALL_SYM + ")" + "*" + "'"),
    Token(INEGER_TOKEN, "(" + ALL_DIGITS + ")" + "|" + "(" + "(" + NOT_NULL_DIGITS + ")" + "(" + ALL_DIGITS + ")" + "+" + ")"),
    Token(BOOL_TOKEN, "TRUE|true|True|FALSE|False|false"),
    Token(SEPARATE_TOKEN, "$"),
    Token(ID_TOKEN, "(" + ALL_ALF_LOWERCASE + ")" + "(" + ALL_SYM + ")" + "*"),
    Token(DOT_TOKEN, "."),
    Token(ASSIGN_TOKEN, ":="),
]

tokensMap = {token.id: token for token in tokens}

SpaceToken = EmptyToken(" ")
TabToken = EmptyToken("(    )")

VarToken = ConcreteToken(tokensMap[KWORD_TOKEN], "VAR")
BeginToken = ConcreteToken(tokensMap[KWORD_TOKEN], "BEGIN")
EndToken = ConcreteToken(tokensMap[KWORD_TOKEN], "END")
DotToken = tokensMap[DOT_TOKEN]
TypeToken = tokensMap[TYPE_TOKEN]
IDToken = tokensMap[ID_TOKEN]
IntegerToken = tokensMap[INEGER_TOKEN]
BoolToken = tokensMap[BOOL_TOKEN]
AssignToken = tokensMap[ASSIGN_TOKEN]
LiteralToken = tokensMap[LITERAL_TOKEN]
EndLineToken = ConcreteToken(tokensMap[SEPARATE_TOKEN], "$")
