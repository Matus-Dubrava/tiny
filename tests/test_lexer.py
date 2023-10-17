import sys

print(sys.path)

from lexer import Lexer, Token, TokenType


def test_lexer():
    input = "let a = 1 + 2;"

    lexer = Lexer(input)

    tokens = [
        Token(TokenType.Let),
        Token(TokenType.Ident, "a"),
        Token(TokenType.Assign),
        Token(TokenType.Int, 1),
        Token(TokenType.Plus),
        Token(TokenType.Int, 2),
        Token(TokenType.Semicolon),
        Token(TokenType.Eof),
    ]

    for expected_token in tokens:
        tok = lexer.next_token()
        assert tok == expected_token, f"expected `{expected_token}`, got `{tok}`"
