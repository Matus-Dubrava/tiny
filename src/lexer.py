from enum import Enum, unique
from dataclasses import dataclass
from typing import Dict, Optional


@unique
class TokenType(str, Enum):
    Let = "LET"
    Plus = "+"
    Minus = "-"
    Asterisk = "*"
    Slash = "/"
    Ident = "IDENT"
    Int = "INT"
    Assign = "="
    Eof = ""
    Semicolon = ";"
    Bang = "!"
    Invalid = "INVALID"
    TRUE = "TRUE"
    FALSE = "FALSE"
    LBrace = "{"
    RBrace = "}"
    LParen = "("
    RParen = ")"
    Comma = ","
    EQ = "=="
    NotEQ = "!="
    LT = "<"
    GT = ">"
    Function = "FUNCTION"
    If = "IF"
    Else = "ELSE"
    Return = "RETURN"
    LBracket = "["
    RBracket = "]"
    String = "STRING"
    Colon = ":"


@dataclass
class Token:
    token_type: TokenType
    literal: Optional[str] = None

    def __eq__(self, other: "Token") -> bool:
        return self.token_type == other.token_type and self.literal == other.literal


INVALID = Token(TokenType.Invalid)

keywords: Dict[str, Token] = {
    "let": Token(TokenType.Let),
    "true": Token(TokenType.TRUE),
    "false": Token(TokenType.FALSE),
    "fn": Token(TokenType.Function),
    "if": Token(TokenType.If),
    "else": Token(TokenType.Else),
    "return": Token(TokenType.Return),
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
        return Token(TokenType.Int, self.input[position : self.position])

    def read_two_char_token(self) -> Token | None:
        if self.ch == "=" and self.peek_char() == "=":
            self.read_char()
            return Token(TokenType.EQ)
        if self.ch == "!" and self.peek_char() == "=":
            self.read_char()
            return Token(TokenType.NotEQ)

    def read_identifier_or_keyword(self) -> Token:
        position = self.position
        while self.ch.isalpha() or self.ch == "_" or self.ch.isnumeric():
            self.read_char()

        ident = self.input[position : self.position]

        if ident in keywords:
            return keywords[ident]
        else:
            return Token(TokenType.Ident, self.input[position : self.position])

    def read_string(self) -> Token:
        self.read_char()
        position = self.position
        while self.ch != '"':
            self.read_char()

        self.read_char()
        string = self.input[position : self.position - 1]
        print(string)
        return Token(TokenType.String, string)

    def next_token(self) -> Token:
        self.eat_whitespace()

        tok = Token(TokenType.Invalid)

        if self.ch == "+":
            tok = Token(TokenType.Plus)
        if self.ch == "-":
            tok = Token(TokenType.Minus)
        if self.ch == "/":
            tok = Token(TokenType.Slash)
        if self.ch == "*":
            tok = Token(TokenType.Asterisk)
        elif self.ch == "(":
            tok = Token(TokenType.LParen)
        elif self.ch == ")":
            tok = Token(TokenType.RParen)
        elif self.ch == "{":
            tok = Token(TokenType.LBrace)
        elif self.ch == "}":
            tok = Token(TokenType.RBrace)
        elif self.ch == ",":
            tok = Token(TokenType.Comma)
        elif self.ch == "<":
            tok = Token(TokenType.LT)
        elif self.ch == ">":
            tok = Token(TokenType.GT)
        elif self.ch == "[":
            tok = Token(TokenType.LBracket)
        elif self.ch == "]":
            tok = Token(TokenType.RBracket)
        elif self.ch == ":":
            tok = Token(TokenType.Colon)
        elif self.ch == '"':
            return self.read_string()
        elif self.ch == "\0":
            tok = Token(TokenType.Eof)
        elif self.ch == ";":
            tok = Token(TokenType.Semicolon)
        elif self.ch == "!":
            res = self.read_two_char_token()
            if res:
                tok = res
            else:
                tok = Token(TokenType.Bang)
        elif self.ch == "=":
            res = self.read_two_char_token()
            if res:
                tok = res
            else:
                tok = Token(TokenType.Assign)
        elif self.ch.isnumeric():
            return self.read_integer()
        elif self.ch.isalpha() or self.ch == "_":
            return self.read_identifier_or_keyword()

        self.read_char()
        return tok


if __name__ == "__main__":
    input = """
        {"foo": "bar"};
    """

    lexer = Lexer(input)
    tok = lexer.next_token()
    tok = lexer.next_token()
    print(tok)
