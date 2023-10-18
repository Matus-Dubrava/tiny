import sys

print(sys.path)

from lexer import Lexer, Token, TokenType


def test_lexer():
    input = """
        let five = 5;
        let ten = 10;
        let add = fn(x, y) {
            x + y;
        };
        let result = add(five, ten);
        !-/*5;
        5 < 10 > 5;
        if (5 < 10) {
            return true;
        } else {
            return false;
        }

        10 == 10;
        10 != 9;
        [1, 2];
        {"foo": "bar"};
        =+(){},;

        x;
        xy_;
        __add__;
        __ADD_x;
        add2;
        add1AND2;
    """

    lexer = Lexer(input)

    tokens = [
        Token(0, 0, TokenType.Let),
        Token(0, 0, TokenType.Ident, "five"),
        Token(0, 0, TokenType.Assign),
        Token(0, 0, TokenType.Int, "5"),
        Token(0, 0, TokenType.Semicolon),
        Token(0, 0, TokenType.Let),
        Token(0, 0, TokenType.Ident, "ten"),
        Token(0, 0, TokenType.Assign),
        Token(0, 0, TokenType.Int, "10"),
        Token(0, 0, TokenType.Semicolon),
        Token(0, 0, TokenType.Let),
        Token(0, 0, TokenType.Ident, "add"),
        Token(0, 0, TokenType.Assign),
        Token(0, 0, TokenType.Function),
        Token(0, 0, TokenType.LParen),
        Token(0, 0, TokenType.Ident, "x"),
        Token(0, 0, TokenType.Comma),
        Token(0, 0, TokenType.Ident, "y"),
        Token(0, 0, TokenType.RParen),
        Token(0, 0, TokenType.LBrace),
        Token(0, 0, TokenType.Ident, "x"),
        Token(0, 0, TokenType.Plus),
        Token(0, 0, TokenType.Ident, "y"),
        Token(0, 0, TokenType.Semicolon),
        Token(0, 0, TokenType.RBrace),
        Token(0, 0, TokenType.Semicolon),
        Token(0, 0, TokenType.Let),
        Token(0, 0, TokenType.Ident, "result"),
        Token(0, 0, TokenType.Assign),
        Token(0, 0, TokenType.Ident, "add"),
        Token(0, 0, TokenType.LParen),
        Token(0, 0, TokenType.Ident, "five"),
        Token(0, 0, TokenType.Comma),
        Token(0, 0, TokenType.Ident, "ten"),
        Token(0, 0, TokenType.RParen),
        Token(0, 0, TokenType.Semicolon),
        Token(0, 0, TokenType.Bang),
        Token(0, 0, TokenType.Minus),
        Token(0, 0, TokenType.Slash),
        Token(0, 0, TokenType.Asterisk),
        Token(0, 0, TokenType.Int, "5"),
        Token(0, 0, TokenType.Semicolon),
        Token(0, 0, TokenType.Int, "5"),
        Token(0, 0, TokenType.LT),
        Token(0, 0, TokenType.Int, "10"),
        Token(0, 0, TokenType.GT),
        Token(0, 0, TokenType.Int, "5"),
        Token(0, 0, TokenType.Semicolon),
        Token(0, 0, TokenType.If),
        Token(0, 0, TokenType.LParen),
        Token(0, 0, TokenType.Int, "5"),
        Token(0, 0, TokenType.LT),
        Token(0, 0, TokenType.Int, "10"),
        Token(0, 0, TokenType.RParen),
        Token(0, 0, TokenType.LBrace),
        Token(0, 0, TokenType.Return),
        Token(0, 0, TokenType.TRUE),
        Token(0, 0, TokenType.Semicolon),
        Token(0, 0, TokenType.RBrace),
        Token(0, 0, TokenType.Else),
        Token(0, 0, TokenType.LBrace),
        Token(0, 0, TokenType.Return),
        Token(0, 0, TokenType.FALSE),
        Token(0, 0, TokenType.Semicolon),
        Token(0, 0, TokenType.RBrace),
        Token(0, 0, TokenType.Int, "10"),
        Token(0, 0, TokenType.EQ),
        Token(0, 0, TokenType.Int, "10"),
        Token(0, 0, TokenType.Semicolon),
        Token(0, 0, TokenType.Int, "10"),
        Token(0, 0, TokenType.NotEQ),
        Token(0, 0, TokenType.Int, "9"),
        Token(0, 0, TokenType.Semicolon),
        Token(0, 0, TokenType.LBracket),
        Token(0, 0, TokenType.Int, "1"),
        Token(0, 0, TokenType.Comma),
        Token(0, 0, TokenType.Int, "2"),
        Token(0, 0, TokenType.RBracket),
        Token(0, 0, TokenType.Semicolon),
        Token(0, 0, TokenType.LBrace),
        Token(0, 0, TokenType.String, "foo"),
        Token(0, 0, TokenType.Colon),
        Token(0, 0, TokenType.String, "bar"),
        Token(0, 0, TokenType.RBrace),
        Token(0, 0, TokenType.Semicolon),
        Token(0, 0, TokenType.Assign),
        Token(0, 0, TokenType.Plus),
        Token(0, 0, TokenType.LParen),
        Token(0, 0, TokenType.RParen),
        Token(0, 0, TokenType.LBrace),
        Token(0, 0, TokenType.RBrace),
        Token(0, 0, TokenType.Comma),
        Token(0, 0, TokenType.Semicolon),
        Token(0, 0, TokenType.Ident, "x"),
        Token(0, 0, TokenType.Semicolon),
        Token(0, 0, TokenType.Ident, "xy_"),
        Token(0, 0, TokenType.Semicolon),
        Token(0, 0, TokenType.Ident, "__add__"),
        Token(0, 0, TokenType.Semicolon),
        Token(0, 0, TokenType.Ident, "__ADD_x"),
        Token(0, 0, TokenType.Semicolon),
        Token(0, 0, TokenType.Ident, "add2"),
        Token(0, 0, TokenType.Semicolon),
        Token(0, 0, TokenType.Ident, "add1AND2"),
        Token(0, 0, TokenType.Semicolon),
        Token(0, 0, TokenType.Eof),
    ]

    for expected_token in tokens:
        tok = lexer.next_token()
        assert tok == expected_token, f"expected `{expected_token}`, got `{tok}`"


def test_token_postions():
    input = """
let five = 5;
let ten = 10;
let add = fn(x, y) {
    x + y;
};
let result = add(five, ten);
!-/*5;
"""

    lexer = Lexer(input)

    tokens = [
        Token(2, 1, TokenType.Let),
        Token(2, 5, TokenType.Ident, "five"),
        Token(2, 10, TokenType.Assign),
        Token(2, 12, TokenType.Int, "5"),
        Token(2, 13, TokenType.Semicolon),
        Token(3, 1, TokenType.Let),
        Token(3, 5, TokenType.Ident, "ten"),
        Token(3, 9, TokenType.Assign),
        Token(3, 11, TokenType.Int, "10"),
        Token(3, 13, TokenType.Semicolon),
        Token(4, 1, TokenType.Let),
        Token(4, 5, TokenType.Ident, "add"),
        Token(4, 9, TokenType.Assign),
        Token(4, 11, TokenType.Function),
        Token(4, 13, TokenType.LParen),
        Token(4, 14, TokenType.Ident, "x"),
        Token(4, 15, TokenType.Comma),
        Token(4, 17, TokenType.Ident, "y"),
        Token(4, 18, TokenType.RParen),
        Token(4, 20, TokenType.LBrace),
        Token(5, 5, TokenType.Ident, "x"),
        Token(5, 7, TokenType.Plus),
        Token(5, 9, TokenType.Ident, "y"),
        Token(5, 10, TokenType.Semicolon),
        Token(6, 1, TokenType.RBrace),
        Token(6, 2, TokenType.Semicolon),
        Token(7, 1, TokenType.Let),
        Token(7, 5, TokenType.Ident, "result"),
        Token(7, 12, TokenType.Assign),
        Token(7, 14, TokenType.Ident, "add"),
        Token(7, 17, TokenType.LParen),
        Token(7, 18, TokenType.Ident, "five"),
        Token(7, 22, TokenType.Comma),
        Token(7, 24, TokenType.Ident, "ten"),
        Token(7, 27, TokenType.RParen),
        Token(7, 28, TokenType.Semicolon),
        Token(8, 1, TokenType.Bang),
        Token(8, 2, TokenType.Minus),
        Token(8, 3, TokenType.Slash),
        Token(8, 4, TokenType.Asterisk),
        Token(8, 5, TokenType.Int, "5"),
        Token(8, 6, TokenType.Semicolon),
        Token(9, 1, TokenType.Eof),
    ]

    for expected_token in tokens:
        tok = lexer.next_token()
        assert tok.compare(expected_token), f"expected `{expected_token}`, got `{tok}`"
