import sys
from lexer import *
from typing import Callable, TextIO


def getDataGetter(f: TextIO) -> Callable[[], str]:
    return lambda: f.readline()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python Lexer.py <input_file> <output_file>")
        sys.exit(1)

    inputFile = sys.argv[1]
    outputFile = sys.argv[2]

    with open(inputFile, 'r', encoding='utf-8') as f:
        lexer = Lexer(list(TOKENS.keys()), getDataGetter(f))
        with open(outputFile, 'w', encoding='utf-8') as output:
            while True:
                token = lexer.nextToken()

                if token is None:
                    break
                if token.name == "LINE_COMMENT" or token.name == "BLOCK_COMMENT":
                    continue

                result = f"{token.name} ({token.lineNumber}, {token.startPosition}) \"{token.value}\""

                print(result)
                output.write(result + "\n")
