from expressions import *

expressions = [
    # BEGIN-EDN
    Expression([BeginToken]),
    Expression([EndToken, DotToken]),

    # VAR
    Expression([SpacesToken, VarToken, SpaceToken, TypeToken, SpaceToken, IDToken, EndLineToken]),

    # ASSIGN
    Expression([SpacesToken, IDToken, SpaceToken, AssignToken, SpaceToken, FloatToken, EndLineToken]),
    Expression([SpacesToken, IDToken, SpaceToken, AssignToken, SpaceToken, IntegerToken, EndLineToken]),
    Expression([SpacesToken, IDToken, SpaceToken, AssignToken, SpaceToken, BoolToken, EndLineToken]),
    Expression([SpacesToken, IDToken, SpaceToken, AssignToken, SpaceToken, LiteralToken, EndLineToken]),
    Expression([SpacesToken, IDToken, SpaceToken, AssignToken, SpaceToken, IDToken, EndLineToken]),

    # COMMENT
    Expression([SpacesToken, CommentToken]),

    # FUNC
    Expression([SpacesToken, WriteToken, LeftRoundBracketToken, IDToken, RightRoundBracketToken, EndLineToken]),
    Expression([SpacesToken, WriteToken, LeftRoundBracketToken, LiteralToken, RightRoundBracketToken, EndLineToken]),
    Expression([SpacesToken, ReadToken, EndLineToken]),
    Expression([SpacesToken, ReadToken, LeftRoundBracketToken, RightRoundBracketToken, EndLineToken]),
    Expression([SpacesToken, ReadToken, LeftRoundBracketToken, IDToken, RightRoundBracketToken, EndLineToken]),
    Expression([SpacesToken, WritelnToken, EndLineToken]),
    Expression([SpacesToken, WritelnToken, LeftRoundBracketToken, IDToken, RightRoundBracketToken, EndLineToken]),
    Expression([SpacesToken, WritelnToken, LeftRoundBracketToken, LiteralToken, RightRoundBracketToken, EndLineToken]),
    Expression([SpacesToken, ReadlnToken, EndLineToken]),
    Expression([SpacesToken, ReadlnToken, LeftRoundBracketToken, IDToken, RightRoundBracketToken, EndLineToken]),
    Expression([SpacesToken, ReadlnToken, LeftRoundBracketToken, RightRoundBracketToken, EndLineToken]),

    # EMPTY
    Expression([SpacesToken])
]
