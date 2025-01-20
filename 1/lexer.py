from __future__ import annotations

from typing import Callable, List
from tokens import Token, TokenProcessResult
from tokensdata import SEPARATOR


class LexerToken:
    def __init__(self, lexerType: str, value: str, pos: (int, int)):
        self.type = lexerType
        self.value = value
        self.pos = pos

    def __repr__(self):
        return f'{self.type} {self.pos} "{self.value}"'


class Lexer:
    def __init__(self, tokens: List[Token], valueGetter: Callable[[], str]):
        self.valueGetter = valueGetter
        self.tokens = tokens
        self.buffer = valueGetter()
        self.line = 1
        self.column = 1
        self.isBad = False

    def nextToken(self) -> LexerToken | None:
        if self.isBad:
            return None
        if len(self.buffer) == 0 and not self.appendNewBufferValue():
            return None


        needContinie = True
        while needContinie:
            needContinie = False
            for token in self.tokens:
                token.reset()

                bufferIndex = 0
                tmpResult = ""

                while True:
                    charResult = token.nextChar(self.buffer[bufferIndex])
                    if charResult == TokenProcessResult.SUCCESS:
                        tmpResult += self.buffer[bufferIndex]
                        bufferIndex += 1
                    if charResult == TokenProcessResult.END or (charResult == TokenProcessResult.SUCCESS and token.isEnd() and bufferIndex == len(self.buffer) and not self.appendNewBufferValue()):
                        tmpBuff = self.buffer
                        self.buffer = self.buffer[bufferIndex:]
                        self.column += len(tmpResult)

                        if tmpResult == "\n":
                            self.column = 1
                            self.line += tmpResult.count("\n")

                        column = self.column
                        line = self.line

                        if token.isCorrectLexema(tmpResult, self.buffer[0] in SEPARATOR):
                            self.setIsLastBeSeparate(token.isSeparate)
                            return LexerToken(token.id, tmpResult, (line, column))
                        self.isBad = True
                        return self.getBad(line, column, tmpBuff, tmpResult)
                    if charResult == TokenProcessResult.MISS:
                        self.buffer = self.buffer[bufferIndex:]
                        self.column = 1
                        self.line += tmpResult.count("\n")

                        self.setIsLastBeSeparate(token.isSeparate)

                        self.column += len(tmpResult)
                        needContinie = True
                        break
                    if charResult == TokenProcessResult.FAILED:
                        break
                    if bufferIndex == len(self.buffer) and not self.appendNewBufferValue():
                        break

        self.isBad = True
        tmp = self.buffer
        return self.getBad(self.line, self.column, tmp)

    def appendNewBufferValue(self) -> bool:
        data = self.valueGetter()
        if len(data) == 0:
            return False
        self.buffer += data
        return True

    def getBad(self, line: int, column: int, buffer: str, lexem = None) -> LexerToken:
        tmp = buffer
        for sep in SEPARATOR:
            tmp = tmp.replace(sep, " ")
        if lexem is None:
            return LexerToken("BAD", tmp.split(" ")[0], (self.line, self.column))
        return LexerToken("BAD", tmp.split(" ")[0], (line, column - len(lexem) -1))

    def setIsLastBeSeparate(self, v: bool):
        self.isLastBeSeparate = v


