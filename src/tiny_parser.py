from lexer import Token, Lexer, ILLEGAL


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.token: Token = ILLEGAL
