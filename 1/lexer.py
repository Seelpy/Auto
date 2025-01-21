from typing import Callable, List
import re
from tokensdata import *
from keywordsdata import *
from sepearatorsdata import *
from operatorsdata import *
from token import *


class Lexer:
    def __init__(self, tokens: List[str], valueGetter: Callable[[], str]):
        self.valueGetter = valueGetter
        self.tokens = tokens
        self.buffer = self.valueGetter()
        self.lineNumber = 1
        self.position = -1
        self.currentChar = None
        self.currentValue = None
        self.startPosition = -1
        self.startLine = 0

    def nextLine(self):
        self.buffer = self.valueGetter()
        if self.buffer:
            self.buffer = self.buffer.replace("\xa0", " ")
            self.lineNumber += 1
            self.position = -1
            return True
        else:
            self.buffer = ""
            return False

    def tryGetNextChar(self):
        self.position += 1
        if self.position >= len(self.buffer):
            return False

        self.currentChar = self.buffer[self.position]
        return True

    def goBack(self):
        self.position -= 1
        self.currentChar = self.buffer[self.position]

    def showNextChar(self):
        try:
            char = self.buffer[self.position + 1]
            return char
        except Exception:
            return None

    def createToken(self, name: str):
        value = self.currentValue
        self.currentValue = None
        start = self.startPosition
        self.startPosition = self.position
        return Token(name, self.startLine, start + 1, value)

    def parseBlockComment(self):
        self.startPosition = self.position
        self.startLine = self.lineNumber
        self.currentValue = self.currentChar
        while True:
            if not self.tryGetNextChar():
                while True:
                    if not self.nextLine():
                        return self.createToken("BAD")
                    if len(self.buffer) > 0:
                        break
                self.tryGetNextChar()

            self.currentValue += self.currentChar
            if self.currentChar == "}":
                return self.createToken("BLOCK_COMMENT")

    def parseString(self, endChar: str):
        self.currentValue = self.currentChar
        self.startPosition = self.position
        self.startLine = self.lineNumber
        while True:
            if self.tryGetNextChar():
                self.currentValue += self.currentChar
                if self.currentChar == endChar:
                    return self.createToken("STRING")

            else:
                return self.createToken("BAD")

    def parseDivide(self):
        self.currentValue = self.currentChar
        self.startPosition = self.position
        self.startLine = self.lineNumber

        nextChar = self.showNextChar()

        if nextChar is not None:
            if nextChar == "/":
                while self.tryGetNextChar():
                    self.currentValue += self.currentChar
                return self.createToken("LINE_COMMENT")
            else:
                return self.createToken("DIVIDE")
        else:
            return self.createToken("DIVIDE")

    def parseDigit(self):
        self.initializeDigitParsing()
        while True:
            if not self.tryGetNextChar():
                self.handleEndOfLine()
                break

            if self.currentChar.isdigit():
                self.appendToCurrentValue()
                continue

            if self.currentChar == ".":
                if not self.handleDotInDigit():
                    break
                continue

            if self.currentChar in SEPARATORS:
                if not self.handleSeparatorInDigit():
                    break
                continue

            if self.currentChar in OPERATORS:
                self.handleOperatorInDigit()
                break

            self.appendToCurrentValue()

        return self.finalizeDigitParsing()

    def initializeDigitParsing(self):
        self.currentValue = self.currentChar
        self.startPosition = self.position
        self.startLine = self.lineNumber
        self.regexFloat = re.compile(TOKENS["FLOAT"])
        self.regexInteger = re.compile(TOKENS["INTEGER"])

    def appendToCurrentValue(self):
        self.currentValue += self.currentChar

    def handleEndOfLine(self):
        self.goBack()

    def handleDotInDigit(self):
        nextChar = self.showNextChar()
        if nextChar is not None:
            if nextChar == ".":
                self.goBack()
                return False
            else:
                self.appendToCurrentValue()
                return True
        else:
            self.appendToCurrentValue()
            return False

    def handleSeparatorInDigit(self):
        if (self.currentValue[-1] == "e" or self.currentValue[-1] == "E") and (
                self.currentChar == "-" or self.currentChar == "+"):
            self.appendToCurrentValue()
            return True
        else:
            self.goBack()
            return False

    def handleOperatorInDigit(self):
        self.goBack()

    def finalizeDigitParsing(self):
        if self.regexFloat.fullmatch(self.currentValue):
            return self.createToken("FLOAT")

        if self.regexInteger.fullmatch(self.currentValue):
            if len(self.currentValue) > 20:
                return self.createToken("BAD")
            return self.createToken("INTEGER")

        return self.createToken("BAD")

    def parseIdentifier(self):
        self.currentValue = self.currentChar
        self.startPosition = self.position
        self.startLine = self.lineNumber

        while True:
            if self.tryGetNextChar():
                if self.currentChar in SEPARATORS:
                    self.goBack()
                    break
                if self.currentChar in OPERATORS:
                    self.goBack()
                    break
                else:
                    self.currentValue += self.currentChar

            else:
                break

        if len(self.currentValue) > 256:
            return self.createToken("BAD")
        for key in KEYS_WORDS:
            regex = re.compile(KEYS_WORDS[key], re.IGNORECASE)
            if regex.fullmatch(self.currentValue):
                return self.createToken(key)
        return self.createToken("BAD")

    def getСharРandlers(self):
        return {
            '{': self.parseBlockComment,
            '"': lambda: self.parseString('"'),
            "'": lambda: self.parseString("'"),
            '+': self.handlePlus,
            '-': self.handleMinus,
            '/': self.handleDivide,
            ';': self.handleSemicolon,
            ',': self.handleComma,
            '(': self.handleLeftParen,
            ')': self.handleRightParen,
            '[': self.handleLeftBracket,
            ']': self.handleRightBracket,
            '=': self.handleEqual,
            '*': self.handleMultiplication,
            '<': self.handleLessThan,
            '>': self.handleGreaterThan,
            ':': self.handleColon,
            '.': self.handleDot,
        }

    def nextToken(self):
        handlers = self.getСharРandlers()

        while True:
            if not self.tryGetNextChar():
                while True:
                    if not self.nextLine():
                        return None
                    if len(self.buffer) > 0:
                        break
                self.tryGetNextChar()

            if self.currentChar in handlers:
                return handlers[self.currentChar]()

            if self.currentChar.isspace():
                continue

            if self.currentChar.isdigit():
                return self.parseDigit()

            if self.currentChar.isalpha() or self.currentChar == '_':
                return self.parseIdentifier()

            return Token("BAD", self.lineNumber, self.position, self.currentChar)

    def handlePlus(self):
        self.currentValue = self.currentChar
        self.startPosition = self.position
        self.startLine = self.lineNumber
        return self.createToken("PLUS")

    def handleMinus(self):
        self.currentValue = self.currentChar
        self.startPosition = self.position
        self.startLine = self.lineNumber
        return self.createToken("MINUS")

    def handleDivide(self):
        self.startLine = self.lineNumber
        return self.parseDivide()

    def handleSemicolon(self):
        self.currentValue = self.currentChar
        self.startPosition = self.position
        self.startLine = self.lineNumber
        return self.createToken("SEMICOLON")

    def handleComma(self):
        self.currentValue = self.currentChar
        self.startPosition = self.position
        self.startLine = self.lineNumber
        return self.createToken("COMMA")

    def handleLeftParen(self):
        self.currentValue = self.currentChar
        self.startPosition = self.position
        self.startLine = self.lineNumber
        return self.createToken("LEFT_PAREN")

    def handleRightParen(self):
        self.currentValue = self.currentChar
        self.startPosition = self.position
        self.startLine = self.lineNumber
        return self.createToken("RIGHT_PAREN")

    def handleLeftBracket(self):
        self.currentValue = self.currentChar
        self.startPosition = self.position
        self.startLine = self.lineNumber
        return self.createToken("LEFT_BRACKET")

    def handleRightBracket(self):
        self.currentValue = self.currentChar
        self.startPosition = self.position
        self.startLine = self.lineNumber
        return self.createToken("RIGHT_BRACKET")

    def handleEqual(self):
        self.startPosition = self.position
        self.currentValue = self.currentChar
        self.startLine = self.lineNumber
        return self.createToken("EQ")

    def handleMultiplication(self):
        self.startPosition = self.position
        self.currentValue = self.currentChar
        self.startLine = self.lineNumber
        return self.createToken("MULTIPLICATION")

    def handleLessThan(self):
        self.startPosition = self.position
        self.startLine = self.lineNumber
        nextChar = self.showNextChar()
        if nextChar is not None:
            if nextChar == "=":
                char = self.currentChar + nextChar
                self.tryGetNextChar()
                return Token("LESS_EQ", self.lineNumber, self.startPosition + 1, char)
            if nextChar == '>':
                char = self.currentChar + nextChar
                self.tryGetNextChar()
                return Token("NOT_EQ", self.lineNumber, self.startPosition + 1, char)
        self.currentValue = self.currentChar
        return self.createToken("LESS")

    def handleGreaterThan(self):
        self.startPosition = self.position
        self.startLine = self.lineNumber
        nextChar = self.showNextChar()
        if nextChar == "=":
            char = self.currentChar + nextChar
            self.tryGetNextChar()
            return Token("GREATER_EQ", self.lineNumber, self.startPosition + 1, char)
        self.currentValue = self.currentChar
        return self.createToken("GREATER")

    def handleColon(self):
        self.startPosition = self.position
        self.startLine = self.lineNumber
        if self.showNextChar() is not None and self.showNextChar() == "=":
            self.currentValue = self.currentChar + self.showNextChar()
            self.tryGetNextChar()
            return self.createToken("ASSIGN")
        else:
            self.currentValue = self.currentChar
            return self.createToken("COLON")

    def handleDot(self):
        self.startPosition = self.position
        self.startLine = self.lineNumber
        self.currentValue = self.currentChar
        return self.createToken("DOT")