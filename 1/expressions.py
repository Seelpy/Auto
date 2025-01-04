from __future__ import annotations

from tokens import *
from typing import List


class Expression:
    def __init__(self, ts: List[RegularInterface]):
        self.tokens = ts

    def Proccess(self, string: str) -> int | None:
        start = 0
        for token in self.tokens:
            tokenId, find, errIdx = token.process(string, start)
            token.reset()
            if errIdx is not None:
                return errIdx
            elif len(tokenId) != 0:
                print(tokenId, "(", find, ")")
            start += len(find)
        return None


expressions = [
    Expression([BeginToken]),
    Expression([EndToken, DotToken]),
    Expression([TabToken, VarToken, SpaceToken, TypeToken, SpaceToken, IDToken, EndLineToken]),
    Expression([TabToken, IDToken, SpaceToken, AssignToken, SpaceToken, IDToken]),
    Expression([TabToken, IDToken, SpaceToken, AssignToken, SpaceToken, IntegerToken]),
    Expression([TabToken, IDToken, SpaceToken, AssignToken, SpaceToken, BoolToken]),
    Expression([TabToken, IDToken, SpaceToken, AssignToken, SpaceToken, LiteralToken]),
]
