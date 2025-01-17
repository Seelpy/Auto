from __future__ import annotations
import regtodka
from enum import Enum


class TokenProcessResult(Enum):
    END = 1
    SUCCESS = 2
    FAILED = 3
    MISS = 4

class Token:
    def __init__(self, id: str, reg: str, maxLen: int|None = None, needMiss: bool = False, needAfterSeparate: bool = False, isSeparate: bool = False):
        self.id = id
        self.reg = reg
        self.maxLen = maxLen
        self.needMiss = needMiss
        self.needAfterSeparate = needAfterSeparate
        self.isSeparate = isSeparate
        self.slider = regtodka.RegToDKAConverter().convert(reg)

    def nextChar(self, c: str) -> TokenProcessResult:
        status = TokenProcessResult.SUCCESS

        if self.slider.IsFinal():
            status = TokenProcessResult.END
        try:
            self.slider.Move(c)
        except:
            if self.slider.IsPossibleFinish():
                status = TokenProcessResult.END if not self.needMiss else TokenProcessResult.MISS
            else:
                status = TokenProcessResult.FAILED
        if status in [TokenProcessResult.END, TokenProcessResult.FAILED, TokenProcessResult.MISS]:
            self.slider.Reset()
        return status

    def isEnd(self) -> bool:
        return self.slider.IsPossibleFinish()

    def reset(self):
        self.slider.Reset()

    def isCorrectLexema(self, lexema: str, nextIsSeparate) -> bool:
        if self.maxLen is not None and self.maxLen <= len(lexema):
            return False
        if self.needAfterSeparate and not nextIsSeparate:
            return False
        return True

    def isSeparate(self) -> bool:
        return self.isSeparate


