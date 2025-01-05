from __future__ import annotations

from tokensdata import *
from typing import List


class Expression:
    def __init__(self, ts: List[RegularInterface]):
        self.tokens = ts

    def Proccess(self, string: str) -> int | None:
        start = 0
        result = ""
        for token in self.tokens:
            tokenId, find, errIdx = token.process(string, start)
            if errIdx is not None:
                return errIdx
            elif len(tokenId) != 0:
                result += tokenId + "(" + find + ")" + "\n"
            start += len(find)
        if len(string) > start:
            return start + 1
        print(result, end="")
        return None
