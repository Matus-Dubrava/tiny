from enum import Enum, unique
from dataclasses import dataclass
from typing import Dict, Optional


@unique
class TokenType(str, Enum):
    Let = "LET"
    Plus = "+"
    Ident = "IDENT"
    Int = "INT"
    Assign = "="
    Eof = ""
    Semicolon = ";"
    Bang = "!"
    Invalid = "INVALID"


@dataclass
class Token:
    token_type: TokenType
    literal: Optional[str] = None


INVALID = Token(TokenType.Invalid)

keywords: Dict[str, Token] = {
    "let": Token(
        TokenType.Let,
    )
}


class Lexer:
    def __init__(self, input: str):
        self.position = 0
        self.read_position = 0
        self.input = input
        self.ch = ""
        self.read_char()

    def read_char(self) -> None:
        if self.read_position >= len(self.input):
            self.ch = "\0"
        else:
            self.ch = self.input[self.read_position]

        self.position = self.read_position
        self.read_position += 1

    def peek_char(self) -> str:
        if self.read_position >= len(self.input):
            return "\0"
        else:
            return self.input[self.read_position]

    def eat_whitespace(self) -> None:
        while self.ch == " " or self.ch == "\n" or self.ch == "\t":
            self.read_char()

    def read_integer(self) -> Token:
        position = self.position
        while self.ch.isnumeric():
            self.read_char()
        return Token(TokenType.Int, int(self.input[position : self.position]))

    def read_identifier_or_keyword(self) -> Token:
        position = self.position
        while self.ch.isalpha() or self.ch == "_":
            self.read_char()

        ident = self.input[position : self.position]

        if ident in keywords:
            return keywords[ident]
        else:
            return Token(TokenType.Ident, self.input[position : self.position])

    def next_token(self) -> Token:
        self.eat_whitespace()

        tok = Token(TokenType.Invalid)

        if self.ch == "+":
            tok = Token(TokenType.Plus)
        elif self.ch == "\0":
            tok = Token(TokenType.Eof)
        elif self.ch == ";":
            tok = Token(TokenType.Semicolon)
        elif self.ch == "!":
            tok = Token(TokenType.Bang)
        elif self.ch == "=":
            tok = Token(TokenType.Assign)
        elif self.ch.isnumeric():
            return self.read_integer()
        elif self.ch.isalpha() or self.ch == "_":
            return self.read_identifier_or_keyword()

        self.read_char()
        return tok


if __name__ == "__main__":
    input = "let x = 1;"
    lexer = Lexer(input)

    while True:
        tok = lexer.next_token()
        print(tok)
        if tok.token_type == TokenType.Eof:
            break
