from enum import Enum, unique
from dataclasses import dataclass
from typing import Dict, Optional, Set


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
    Illegal = "ILLEGAL"
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
    line: int
    column: int
    token_type: TokenType
    literal: Optional[str] = None

    def __eq__(self, other: "Token") -> bool:
        """
        When comparing two tokens, by default we are not comparing their position.
        """
        return self.token_type == other.token_type and self.literal == other.literal

    def compare(self, other: "Token") -> bool:
        """
        Compare whether all fields match, including position.
        """
        return self == other and self.column == other.column and self.line == other.line

    def __repr__(self):
        return f"[{self.line},{self.column}] '{self.token_type}' {self.literal}"


class Lexer:
    def __init__(self, input: str):
        self.position = 0
        self.read_position = 0
        self.line = 1
        self.column = 0
        self.input = input
        self.ch = ""
        self.read_char()

    def read_char(self) -> None:
        if self.read_position >= len(self.input):
            self.ch = "\0"
        else:
            self.ch = self.input[self.read_position]

        self.column += 1
        self.position = self.read_position
        self.read_position += 1

    def peek_char(self) -> str:
        if self.read_position >= len(self.input):
            return "\0"
        else:
            return self.input[self.read_position]

    def eat_whitespace(self) -> None:
        while self.ch == " " or self.ch == "\n" or self.ch == "\t":
            if self.ch == "\n":
                self.line += 1
                self.column = 0
            self.read_char()

    def read_integer(self) -> Token:
        position = self.position
        column = self.column
        while self.ch.isnumeric():
            self.read_char()
        return Token(
            self.line, column, TokenType.Int, self.input[position : self.position]
        )

    def read_two_char_token(self) -> Token | None:
        if self.ch == "=" and self.peek_char() == "=":
            self.read_char()
            return Token(self.line, self.column, TokenType.EQ)
        if self.ch == "!" and self.peek_char() == "=":
            self.read_char()
            return Token(self.line, self.column, TokenType.NotEQ)

    def read_identifier_or_keyword(self) -> Token:
        position = self.position
        column = self.column
        while self.ch.isalpha() or self.ch == "_" or self.ch.isnumeric():
            self.read_char()

        ident = self.input[position : self.position]

        if ident == "let":
            return Token(self.line, column, TokenType.Let)
        elif ident == "return":
            return Token(self.line, column, TokenType.Return)
        elif ident == "if":
            return Token(self.line, column, TokenType.If)
        elif ident == "else":
            return Token(self.line, column, TokenType.Else)
        elif ident == "true":
            return Token(self.line, column, TokenType.TRUE)
        elif ident == "false":
            return Token(self.line, column, TokenType.FALSE)
        elif ident == "fn":
            return Token(self.line, column, TokenType.Function)
        else:
            return Token(
                self.line,
                column,
                TokenType.Ident,
                self.input[position : self.position],
            )

    def read_string(self) -> Token:
        self.read_char()
        position = self.position
        while self.ch != '"':
            self.read_char()

        self.read_char()
        string = self.input[position : self.position - 1]
        print(string)
        return Token(self.line, self.column, TokenType.String, string)

    def next_token(self) -> Token:
        self.eat_whitespace()

        if self.ch == "+":
            tok = Token(self.line, self.column, TokenType.Plus)
        if self.ch == "-":
            tok = Token(self.line, self.column, TokenType.Minus)
        if self.ch == "/":
            tok = Token(self.line, self.column, TokenType.Slash)
        if self.ch == "*":
            tok = Token(self.line, self.column, TokenType.Asterisk)
        elif self.ch == "(":
            tok = Token(self.line, self.column, TokenType.LParen)
        elif self.ch == ")":
            tok = Token(self.line, self.column, TokenType.RParen)
        elif self.ch == "{":
            tok = Token(self.line, self.column, TokenType.LBrace)
        elif self.ch == "}":
            tok = Token(self.line, self.column, TokenType.RBrace)
        elif self.ch == ",":
            tok = Token(self.line, self.column, TokenType.Comma)
        elif self.ch == "<":
            tok = Token(self.line, self.column, TokenType.LT)
        elif self.ch == ">":
            tok = Token(self.line, self.column, TokenType.GT)
        elif self.ch == "[":
            tok = Token(self.line, self.column, TokenType.LBracket)
        elif self.ch == "]":
            tok = Token(self.line, self.column, TokenType.RBracket)
        elif self.ch == ":":
            tok = Token(self.line, self.column, TokenType.Colon)
        elif self.ch == '"':
            return self.read_string()
        elif self.ch == "\0":
            tok = Token(self.line, self.column, TokenType.Eof)
        elif self.ch == ";":
            tok = Token(self.line, self.column, TokenType.Semicolon)
        elif self.ch == "!":
            res = self.read_two_char_token()
            if res:
                tok = res
            else:
                tok = Token(self.line, self.column, TokenType.Bang)
        elif self.ch == "=":
            res = self.read_two_char_token()
            if res:
                tok = res
            else:
                tok = Token(self.line, self.column, TokenType.Assign)
        elif self.ch.isnumeric():
            return self.read_integer()
        elif self.ch.isalpha() or self.ch == "_":
            return self.read_identifier_or_keyword()

        self.read_char()
        return tok
