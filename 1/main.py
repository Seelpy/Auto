import lexer
import tokensdata
from typing import TextIO, Callable

def getDataGetter(f: TextIO) ->Callable[[], str]:
    return lambda: f.readline()

if __name__ == "__main__":
    import sys

    if len(sys.argv) not in {3, 4}:
        print("main.py <inFile> <outFile>")
        sys.exit(1)

    inFile = sys.argv[1]
    outFile = sys.argv[2]

    if len(sys.argv) == 4:
        inFile = sys.argv[2]
        outFile = sys.argv[3]



    with open('./data/in.txt', 'r', encoding='utf-8') as f:
        lexer = lexer.Lexer(tokensdata.token_types, getDataGetter(f))
        while (token := lexer.nextToken()) is not None:
            if token.type != "SPACE":
                print(token)
