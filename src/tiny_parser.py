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


precedences: Dict[TokenType, Precedence] = {
    TokenType.Plus: Precedence.Sum,
    TokenType.Minus: Precedence.Sum,
    TokenType.Asterisk: Precedence.Product,
    TokenType.Slash: Precedence.Product,
    TokenType.LT: Precedence.LessGreater,
    TokenType.GT: Precedence.LessGreater,
    TokenType.EQ: Precedence.Equals,
    TokenType.NotEQ: Precedence.Equals,
}

PrefixParseFunction = Callable[[], Union[ast.Node, ParseError]]
InfixParseFunction = Callable[[ast.Node], Union[ast.Node, ParseError]]


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.cur_token: Token = Token(0, 0, TokenType.Illegal)
        self.peek_token: Token = Token(0, 0, TokenType.Illegal)
        self.errors: List[ParseError] = []

        self.prefix_parse_functions: Dict[TokenType, PrefixParseFunction] = {
            TokenType.Int: self.parse_integer,
            TokenType.TRUE: self.parse_boolean,
            TokenType.FALSE: self.parse_boolean,
            TokenType.Bang: self.parse_prefix_expression,
            TokenType.Minus: self.parse_prefix_expression,
            TokenType.Ident: self.parse_identifier,
            TokenType.LParen: self.parse_grouped_expression,
            TokenType.Function: self.parse_function_literal,
        }

        self.infix_parse_functions: Dict[TokenType, InfixParseFunction] = {
            TokenType.Plus: self.parse_infix_expression,
            TokenType.Minus: self.parse_infix_expression,
            TokenType.Asterisk: self.parse_infix_expression,
            TokenType.Slash: self.parse_infix_expression,
            TokenType.LT: self.parse_infix_expression,
            TokenType.GT: self.parse_infix_expression,
            TokenType.EQ: self.parse_infix_expression,
            TokenType.NotEQ: self.parse_infix_expression,
        }

        self.next_token()
        self.next_token()

    def next_token(self) -> None:
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def parse_program(self) -> ast.Program:
        cur_token = self.cur_token
        nodes = self.parse_statements()
        return ast.Program(cur_token, nodes)

    def parse_block_statement(self) -> Union[ast.Node, ParseError]:
        cur_token = self.cur_token
        self.next_token()

        statements: List[ast.Node] = []
        while (
            self.cur_token.token_type != TokenType.RBrace
            and self.cur_token.token_type != TokenType.Eof
        ):
            stmt_or_err = self.parse_statement()
            if isinstance(stmt_or_err, ParseError):
                return stmt_or_err

            statements.append(stmt_or_err)
            self.next_token()

        self.expect_peek_and_advance(TokenType.RBrace)
        return ast.BlockStatement(cur_token, statements)

    def parse_statements(self) -> List[ast.Node]:
        nodes: List[ast.Node] = []
        while self.cur_token.token_type != TokenType.Eof:
            node_or_err = self.parse_statement()

            # Here we are collecting all of the parsing errors.
            if isinstance(node_or_err, ParseError):
                self.errors.append(node_or_err)
            else:
                nodes.append(node_or_err)

            self.next_token()
            if self.cur_token.token_type == TokenType.Semicolon:
                self.next_token()

        return nodes

    def parse_statement(self) -> Union[ast.Node, ParseError]:
        if self.cur_token.token_type == TokenType.Let:
            node_or_err = self.parse_let_statement()
        elif self.cur_token.token_type == TokenType.Return:
            node_or_err = self.parse_return_statement()
        else:
            node_or_err = self.parse_expression(Precedence.Lowest)

        self.read_until_semicolon()

        return node_or_err

    def parse_integer(self) -> ast.Node:
        return ast.IntegerLiteral(self.cur_token, int(self.cur_token.literal))

    def parse_boolean(self) -> ast.Node:
        return ast.BooleanLiteral(
            self.cur_token,
            True if self.cur_token.token_type == TokenType.TRUE else False,
        )

    def parse_function_literal(self) -> Union[ast.Node, ParseError]:
        cur_token = self.cur_token
        self.next_token()

        params_or_err = self.parse_list_of_expressions(TokenType.RParen)
        if isinstance(params_or_err, ParseError):
            return params_or_err

        self.expect_peek_and_advance(TokenType.LBrace)
        block_or_err = self.parse_block_statement()
        if isinstance(block_or_err, ParseError):
            return block_or_err

        self.next_token()

        return ast.Function(cur_token, params_or_err, block_or_err)

    def parse_list_of_expressions(
        self, closing_token: TokenType
    ) -> Union[List[ast.Node], ParseError]:
        expressions: List[ast.Node] = []

        while (
            self.peek_token.token_type != closing_token
            and self.peek_token.token_type != TokenType.Eof
        ):
            self.next_token()
            expr_or_err = self.parse_expression(Precedence.Lowest)
            if isinstance(expr_or_err, ParseError):
                return expr_or_err

            expressions.append(expr_or_err)

            if self.peek_token.token_type == TokenType.Comma:
                self.next_token()

        self.expect_peek_and_advance(closing_token)
        return expressions

    def parse_grouped_expression(self) -> Union[ast.Node, ParseError]:
        self.next_token()

        expr_or_err = self.parse_expression(Precedence.Lowest)
        if isinstance(expr_or_err, ParseError):
            return expr_or_err

        self.expect_peek_and_advance(TokenType.RParen)
        return expr_or_err

    def parse_prefix_expression(self) -> Union[ast.Node, ParseError]:
        cur_tok = self.cur_token

        self.next_token()
        expr_or_error = self.parse_expression(Precedence.Prefix)
        if isinstance(expr_or_error, ParseError):
            return expr_or_error

        return ast.PrefixExpression(cur_tok, cur_tok.token_type.value, expr_or_error)

    def parse_infix_expression(
        self, left_expr: ast.Node
    ) -> Union[ast.Node, ParseError]:
        cur_token = self.cur_token
        cur_precedence = self.get_current_precendence()
        self.next_token()

        right_expr_or_error = self.parse_expression(cur_precedence)
        if isinstance(right_expr_or_error, ParseError):
            return right_expr_or_error

        return ast.InfixExpression(
            cur_token, left_expr, cur_token.token_type.value, right_expr_or_error
        )

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

        left_expr_or_err = prefix_fn()

        while (
            self.peek_token.token_type != TokenType.Semicolon
            and precedence.value < self.get_peek_precedence().value
        ):
            if isinstance(left_expr_or_err, ParseError):
                return left_expr_or_err

            infix_fn = self.infix_parse_functions.get(self.peek_token.token_type)
            if not infix_fn:
                return left_expr_or_err

            self.next_token()

            left_expr_or_err = infix_fn(left_expr_or_err)

        return left_expr_or_err

    def read_until_semicolon(self) -> None:
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

    def get_current_precendence(self) -> Precedence:
        precedence = precedences.get(self.cur_token.token_type)
        if precedence:
            return precedence
        else:
            return Precedence.Lowest

    def get_peek_precedence(self) -> Precedence:
        precedence = precedences.get(self.peek_token.token_type)
        if precedence:
            return precedence
        else:
            return Precedence.Lowest
