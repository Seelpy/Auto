from tokens import *
from typing import List


class Expression:
    def __init__(self, ts: List[RegularInterface]):
        self.tokens = ts

    def Proccess(self, string: str):
        start = 0
        for token in self.tokens:
            token, find, errIdx = token.process(string, start)
            if errIdx != -1:
                break
            elif len(token) != 0:
                print(token, "(", find, ")")
            start += len(find)


expressions = [
    Expression([ConcreteToken(tokensMap[KWORD_TOKEN], "VAR"), EmptyToken(" "), tokensMap[ID_TOKEN]])
]
