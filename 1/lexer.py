from __future__ import annotations

from typing import Callable, List
from tokens import Token, TokenProcessResult


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
        self.column = 0

    def nextToken(self) -> LexerToken | None:
        if len(self.buffer) == 0 and not self.appendNewBufferValue():
            return None

        for token in self.tokens:
            token.reset()

            bufferIndex = 0
            tmpResult = ""

            tmpLine = self.line
            tmpColumn = self.column

            while True:
                if self.buffer[bufferIndex] == "\n":
                    tmpLine += 1
                charResult = token.nextChar(self.buffer[bufferIndex])
                if charResult == TokenProcessResult.SUCCESS:
                    tmpResult += self.buffer[bufferIndex]
                    bufferIndex += 1
                if charResult == TokenProcessResult.END or (charResult == TokenProcessResult.SUCCESS and token.isEnd() and bufferIndex == len(self.buffer) and not self.appendNewBufferValue()):
                    self.line, self.column = tmpLine, tmpColumn
                    self.buffer = self.buffer[bufferIndex:]
                    self.bu = self.buffer[bufferIndex:]
                    return LexerToken(token.id, tmpResult, (self.line, self.column))
                if charResult == TokenProcessResult.FAILED:
                    break


                if bufferIndex == len(self.buffer) and not self.appendNewBufferValue():
                    break

        return LexerToken("BAD", self.buffer[0], (self.line, self.column + 1))

    def appendNewBufferValue(self) -> bool:
        data = self.valueGetter()
        if len(data) == 0:
            return False
        self.buffer += data
        return True

