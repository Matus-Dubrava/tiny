from lexer import Token, Lexer, TokenType
from typing import List, Union, Optional
from dataclasses import dataclass

import abstract_syntaxt_tree as ast


@dataclass
class ParseError:
    line: int
    column: int
    msg: str


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.cur_token: Token = Token(0, 0, TokenType.Illegal)
        self.peek_token: Token = Token(0, 0, TokenType.Illegal)
        self.errors: List[ParseError] = []

        self.next_token()
        self.next_token()

    def next_token(self):
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def parse_program(self) -> ast.Program:
        cur_token = self.cur_token
        statements: List[ast.Node] = []

        while self.cur_token.token_type != TokenType.Eof:
            if self.cur_token.token_type == TokenType.Let:
                stmt_or_error = self.parseLetStatement()
            elif self.cur_token.token_type == TokenType.Return:
                stmt_or_error = self.parseReturnStatement()

            # handle parse errors here
            if isinstance(stmt_or_error, ParseError):
                self.errors.append(stmt_or_error)

            statements.append(stmt_or_error)
            self.next_token()

        return ast.Program(cur_token, statements)

    def parseReturnStatement(self) -> Union[ast.Node, ParseError]:
        cur_tok = self.cur_token
        self.next_token()
        self.read_until_semicolon()
        expr = self.parse_expression()
        return ast.ReturnStatement(cur_tok, expr)

    def parseLetStatement(self) -> Union[ast.Node, ParseError]:
        cur_tok = self.cur_token
        self.next_token()

        ident = self.parse_identifier()
        maybe_err = self.expect_peek_and_advance(TokenType.Assign)
        if maybe_err:
            return maybe_err

        self.next_token()
        expr_or_err = self.parse_expression()
        if isinstance(expr_or_err, ParseError):
            return expr_or_err

        return ast.LetStatement(cur_tok, ident, expr_or_err)

    def parse_expression(self) -> Union[ast.Node, ParseError]:
        cur_tok = self.cur_token
        self.read_until_semicolon()
        expr = ast.DummyExpression(cur_tok)
        return expr

    def read_until_semicolon(self):
        while (
            self.cur_token.token_type != TokenType.Semicolon
            and self.cur_token.token_type != TokenType.Eof
        ):
            self.next_token()

    def expect_peek_and_advance(self, token_type: TokenType) -> Optional[ParseError]:
        if self.peek_token.token_type != token_type:
            return ParseError(
                self.peek_token.line,
                self.peek_token.column,
                f"expected '{token_type}', got {self.peek_token.token_type}",
            )

        self.next_token()
        return None

    def parse_identifier(self):
        return ast.Identifier(self.cur_token, self.cur_token.literal)
