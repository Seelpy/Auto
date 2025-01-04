from abc import ABC, abstractmethod
import regtodka


class RegularInterface(ABC):
    @abstractmethod
    def process(self, string: str, start: int) -> [str, str, int]:
        pass


class Token(RegularInterface):
    def __init__(self, id: str, reg: str):
        self.id = id
        self.reg = reg
        self.slider = regtodka.RegToDKAConverter().convert(reg)

    def process(self, string: str, start: int) -> [str, str, int]:
        i = start
        for c in string[start:]:
            if self.slider.IsFinal():
                break
            try:
                self.slider.Move(c)
            except:
                return "", "", i
            i += 1
        return self.id, string[start: i], -1


class EmptyToken(RegularInterface):
    def __init__(self, reg: str):
        self.reg = reg
        self.slider = regtodka.RegToDKAConverter().convert(reg)

    def process(self, string: str, start: int) -> [str, str, int]:
        i = start
        for c in string[start:]:
            if self.slider.IsFinal():
                break
            try:
                self.slider.Move(c)
            except:
                return "", "", i
            i += 1
        return "", string[start: i], -1


class ConcreteToken(RegularInterface):
    def __init__(self, token: Token, value: str):
        self.token = token
        self.value = value

    def process(self, string: str, start: int) -> [str, str, int]:
        token, val, errIndx = self.token.process(string, start)
        if errIndx != -1:
            return token, val, errIndx
        if val != self.value:
            return token, "", start
        return token, val, -1



ALL_DIGITS = "1|2|3|4|5|6|7|8|9|0"
ALL_ALF_LOWERCASE = "a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z"
ALL_ALF_UPPERCASE = "A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z"
ALL_ALF = ALL_ALF_LOWERCASE + "|" + ALL_ALF_UPPERCASE
ALL_SYM = ALL_ALF + "|" + ALL_DIGITS

KWORD_TOKEN = "KWORD"
SEPARATE_TOKEN = "SEP"
ID_TOKEN = "ID"
DOT_TOKEN = "DOT"
ASSIGN_TOKEN = "ASSIGN"

tokens = [
    Token(KWORD_TOKEN, "VAR|BEGIN|END|WRITE|READ"),
    Token(SEPARATE_TOKEN, ";|,"),
    Token(ID_TOKEN, "(" + ALL_ALF_LOWERCASE + ")" + "(" + ALL_SYM + ")" + "*"),
    Token(DOT_TOKEN, "."),
    Token(ASSIGN_TOKEN, ":="),
]

tokensMap = {token.id: token for token in tokens}
