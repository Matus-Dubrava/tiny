from lexer import Token, Lexer, TokenType
from typing import List, Union, Optional, Callable, Dict
from dataclasses import dataclass
from enum import Enum, unique

import abstract_syntaxt_tree as ast


@dataclass
class ParseError:
    line: int
    column: int
    msg: str


@unique
class Precedence(Enum):
    Lowest = 0
    Assign = 1
    Equals = 2
    LessGreater = 3
    Sum = 4
    Product = 5
    Prefix = 6
    Call = 7
    Index = 8


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.cur_token: Token = Token(0, 0, TokenType.Illegal)
        self.peek_token: Token = Token(0, 0, TokenType.Illegal)
        self.errors: List[ParseError] = []

        self.prefix_parse_functions: Dict[TokenType, Callable] = {
            TokenType.Int: self.parse_integer,
            TokenType.TRUE: self.parse_boolean,
            TokenType.FALSE: self.parse_boolean,
            TokenType.Bang: self.parse_prefix_expression,
            TokenType.Minus: self.parse_prefix_expression,
        }

        self.next_token()
        self.next_token()

    def next_token(self):
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def parse_program(self) -> ast.Program:
        cur_token = self.cur_token
        nodes: List[ast.Node] = []

        while self.cur_token.token_type != TokenType.Eof:
            if self.cur_token.token_type == TokenType.Let:
                node_or_error = self.parse_let_statement()
            elif self.cur_token.token_type == TokenType.Return:
                node_or_error = self.parse_return_statement()
            else:
                node_or_error = self.parse_expression(Precedence.Lowest)

            # handle parse errors here
            if isinstance(node_or_error, ParseError):
                self.errors.append(node_or_error)
            else:
                nodes.append(node_or_error)
            self.next_token()

        return ast.Program(cur_token, nodes)

    def parse_integer(self) -> ast.Node:
        return ast.IntegerLiteral(self.cur_token, int(self.cur_token.literal))

    def parse_boolean(self) -> ast.Node:
        return ast.BooleanLiteral(
            self.cur_token,
            True if self.cur_token.token_type == TokenType.TRUE else False,
        )

    def parse_prefix_expression(self) -> Union[ast.Node, ParseError]:
        cur_tok = self.cur_token

        self.next_token()
        expr_or_error = self.parse_expression(Precedence.Prefix)
        if isinstance(expr_or_error, ParseError):
            return expr_or_error

        return ast.PrefixExpression(cur_tok, cur_tok.token_type.value, expr_or_error)

    def parse_return_statement(self) -> Union[ast.Node, ParseError]:
        cur_tok = self.cur_token
        self.next_token()
        expr_or_error = self.parse_expression(Precedence.Lowest)
        if isinstance(expr_or_error, ParseError):
            return expr_or_error

        self.read_until_semicolon()
        return ast.ReturnStatement(cur_tok, expr_or_error)

    def parse_let_statement(self) -> Union[ast.Node, ParseError]:
        cur_tok = self.cur_token
        self.next_token()

        ident = self.parse_identifier()
        maybe_err = self.expect_peek_and_advance(TokenType.Assign)
        if maybe_err:
            return maybe_err

        self.next_token()
        expr_or_err = self.parse_expression(Precedence.Lowest)
        if isinstance(expr_or_err, ParseError):
            return expr_or_err

        self.read_until_semicolon()
        return ast.LetStatement(cur_tok, ident, expr_or_err)

    def parse_expression(self, precedence: Precedence) -> Union[ast.Node, ParseError]:
        cur_tok = self.cur_token

        prefix_fn = self.prefix_parse_functions.get(self.cur_token.token_type)
        if not prefix_fn:
            return ParseError(
                cur_tok.line,
                cur_tok.column,
                f"no prefix parse function found for '{self.cur_token.token_type}'",
            )

        prefix_expr_or_error = prefix_fn()
        if isinstance(prefix_expr_or_error, ParseError):
            return prefix_expr_or_error

        if self.peek_token.token_type == TokenType.Semicolon:
            self.next_token()

        return prefix_expr_or_error

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
