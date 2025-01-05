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
                    break
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