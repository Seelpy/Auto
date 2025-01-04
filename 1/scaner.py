import expressions
from typing import List

class Scanner:
    def __init__(self, exs: List[expressions.Expression]):
        self.exs = exs
    def process(self, text: str):
        for line in text.splitlines():
            for ex in self.exs:
                ex.Proccess(line)