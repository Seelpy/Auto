class Token:
    def __init__(self, name: str, lineNumber: int, startPosition: int, value: str):
        self.name = name
        self.value = value
        self.lineNumber = lineNumber
        self.startPosition = startPosition