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
        Token(TokenType.Let),
        Token(TokenType.Ident, "five"),
        Token(TokenType.Assign),
        Token(TokenType.Int, "5"),
        Token(TokenType.Semicolon),
        Token(TokenType.Let),
        Token(TokenType.Ident, "ten"),
        Token(TokenType.Assign),
        Token(TokenType.Int, "10"),
        Token(TokenType.Semicolon),
        Token(TokenType.Let),
        Token(TokenType.Ident, "add"),
        Token(TokenType.Assign),
        Token(TokenType.Function),
        Token(TokenType.LParen),
        Token(TokenType.Ident, "x"),
        Token(TokenType.Comma),
        Token(TokenType.Ident, "y"),
        Token(TokenType.RParen),
        Token(TokenType.LBrace),
        Token(TokenType.Ident, "x"),
        Token(TokenType.Plus),
        Token(TokenType.Ident, "y"),
        Token(TokenType.Semicolon),
        Token(TokenType.RBrace),
        Token(TokenType.Semicolon),
        Token(TokenType.Let),
        Token(TokenType.Ident, "result"),
        Token(TokenType.Assign),
        Token(TokenType.Ident, "add"),
        Token(TokenType.LParen),
        Token(TokenType.Ident, "five"),
        Token(TokenType.Comma),
        Token(TokenType.Ident, "ten"),
        Token(TokenType.RParen),
        Token(TokenType.Semicolon),
        Token(TokenType.Bang),
        Token(TokenType.Minus),
        Token(TokenType.Slash),
        Token(TokenType.Asterisk),
        Token(TokenType.Int, "5"),
        Token(TokenType.Semicolon),
        Token(TokenType.Int, "5"),
        Token(TokenType.LT),
        Token(TokenType.Int, "10"),
        Token(TokenType.GT),
        Token(TokenType.Int, "5"),
        Token(TokenType.Semicolon),
        Token(TokenType.If),
        Token(TokenType.LParen),
        Token(TokenType.Int, "5"),
        Token(TokenType.LT),
        Token(TokenType.Int, "10"),
        Token(TokenType.RParen),
        Token(TokenType.LBrace),
        Token(TokenType.Return),
        Token(TokenType.TRUE),
        Token(TokenType.Semicolon),
        Token(TokenType.RBrace),
        Token(TokenType.Else),
        Token(TokenType.LBrace),
        Token(TokenType.Return),
        Token(TokenType.FALSE),
        Token(TokenType.Semicolon),
        Token(TokenType.RBrace),
        Token(TokenType.Int, "10"),
        Token(TokenType.EQ),
        Token(TokenType.Int, "10"),
        Token(TokenType.Semicolon),
        Token(TokenType.Int, "10"),
        Token(TokenType.NotEQ),
        Token(TokenType.Int, "9"),
        Token(TokenType.Semicolon),
        Token(TokenType.LBracket),
        Token(TokenType.Int, "1"),
        Token(TokenType.Comma),
        Token(TokenType.Int, "2"),
        Token(TokenType.RBracket),
        Token(TokenType.Semicolon),
        Token(TokenType.LBrace),
        Token(TokenType.String, "foo"),
        Token(TokenType.Colon),
        Token(TokenType.String, "bar"),
        Token(TokenType.RBrace),
        Token(TokenType.Semicolon),
        Token(TokenType.Assign),
        Token(TokenType.Plus),
        Token(TokenType.LParen),
        Token(TokenType.RParen),
        Token(TokenType.LBrace),
        Token(TokenType.RBrace),
        Token(TokenType.Comma),
        Token(TokenType.Semicolon),
        Token(TokenType.Ident, "x"),
        Token(TokenType.Semicolon),
        Token(TokenType.Ident, "xy_"),
        Token(TokenType.Semicolon),
        Token(TokenType.Ident, "__add__"),
        Token(TokenType.Semicolon),
        Token(TokenType.Ident, "__ADD_x"),
        Token(TokenType.Semicolon),
        Token(TokenType.Ident, "add2"),
        Token(TokenType.Semicolon),
        Token(TokenType.Ident, "add1AND2"),
        Token(TokenType.Semicolon),
        Token(TokenType.Eof),
    ]

    for expected_token in tokens:
        tok = lexer.next_token()
        assert tok == expected_token, f"expected `{expected_token}`, got `{tok}`"
