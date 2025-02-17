TOKENS = {
    "WHITESPACE": r"\s",
    "LINE_COMMENT": r"//.*",
    "BLOCK_COMMENT": r"\{(?:.|\n)*?\}",
    "START_BLOCK_COMMENT": r"\{\s*.*",
    "END_BLOCK_COMMENT": r"(?:.|\n)*?\}",
    "IDENTIFIER": r"[a-zA-Z_][a-zA-Z0-9_]*",
    "STRING": r"'(?:[^'\\]|\\.)*'",
    "INTEGER": r"^(?<![\d.])\b\d+\b(?![\d.])$",
    "FLOAT": r"^\d+\.\d+([eE][+-]?\d+)?$|^\d+[e|E][+-]?\d+$",
    "PLUS": r"\+",
    "MINUS": r"-",
    "DIVIDE": r"/",
    "SEMICOLON": r";",
    "COMMA": r",",
    "LEFT_PAREN": r"\(",
    "RIGHT_PAREN": r"\)",
    "LEFT_BRACKET": r"\[",
    "RIGHT_BRACKET": r"\]",
    "EQ": r"=",
    "GREATER": r">",
    "LESS": r"<",
    "LESS_EQ": r"<=",
    "GREATER_EQ": r">=",
    "NOT_EQ": r"<>",
    "COLON": r":",
    "ASSIGN": r":=",
    "DOT": r"\.",
}