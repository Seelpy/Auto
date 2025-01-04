import expressions
from typing import List


class Scanner:
    def __init__(self, exs: List[expressions.Expression]):
        self.exs = exs

    def process(self, text: str):
        lineIdx = 1
        for line in text.splitlines():
            errIdx = None
            for ex in self.exs:
                errIdxtmp = ex.Proccess(line)
                if errIdxtmp is not None:
                    errIdx = errIdxtmp
                else:
                    errIdx = None
                    break

            if errIdx is not None:
                print("ERROR", "(", lineIdx, ":", errIdx, ")")
                return
            lineIdx += 1
