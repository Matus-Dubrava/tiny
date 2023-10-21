from dataclasses import dataclass
from enum import Enum, unique
from typing import Callable, Dict, List, Optional, Tuple, Union

import abstract_syntaxt_tree as ast
from lexer import Lexer, Token, TokenType

DEBUG = True


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
    TokenType.LParen: Precedence.Call,
    TokenType.LBracket: Precedence.Index,
}

PrefixParseFunction = Callable[[int], Union[ast.Node, ParseError]]
InfixParseFunction = Callable[[ast.Node, int], Union[ast.Node, ParseError]]


def show_parse_info(depth: int, node_name: str, cur_token: Token) -> None:
    if DEBUG:
        print("".join(["\t"] * depth) + f" {node_name}: token: {cur_token}")


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
            TokenType.If: self.parse_if_expression,
            TokenType.LBracket: self.parse_array_literal,
            TokenType.String: self.parse_string_literal,
            TokenType.LBrace: self.parse_hash_literal,
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
            TokenType.LParen: self.parse_call_expression,
            TokenType.LBracket: self.parse_index_expression,
        }

        self.next_token()
        self.next_token()

    def next_token(self) -> None:
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def parse_program(self) -> ast.Program:
        cur_token = self.cur_token
        nodes = self.parse_statements(depth=0)
        return ast.Program(cur_token, nodes)

    def parse_block_statement(self, depth: int) -> Union[ast.Node, ParseError]:
        cur_token = self.cur_token
        self.next_token()

        statements: List[ast.Node] = []
        while (
            self.cur_token.token_type != TokenType.RBrace
            and self.cur_token.token_type != TokenType.Eof
        ):
            stmt_or_err = self.parse_statement(depth)
            if isinstance(stmt_or_err, ParseError):
                return stmt_or_err

            statements.append(stmt_or_err)
            self.next_token()

        self.expect_peek_and_advance(TokenType.RBrace)
        return ast.BlockStatement(cur_token, statements)

    def parse_statements(self, depth: int) -> List[ast.Node]:
        nodes: List[ast.Node] = []
        while self.cur_token.token_type != TokenType.Eof:
            node_or_err = self.parse_statement(depth)

            # Here we are collecting all of the parsing errors.
            if isinstance(node_or_err, ParseError):
                self.errors.append(node_or_err)
            else:
                nodes.append(node_or_err)

            self.next_token()
            if self.cur_token.token_type == TokenType.Semicolon:
                self.next_token()

        return nodes

    def parse_statement(self, depth: int) -> Union[ast.Node, ParseError]:
        if self.cur_token.token_type == TokenType.Let:
            node_or_err = self.parse_let_statement(depth)
        elif self.cur_token.token_type == TokenType.Return:
            node_or_err = self.parse_return_statement(depth)
        else:
            node_or_err = self.parse_expression(Precedence.Lowest, depth)

        if self.peek_token.token_type == TokenType.Semicolon:
            self.next_token()

        return node_or_err

    def parse_integer(self, depth: int) -> ast.Node:
        show_parse_info(depth, "INTEGER", self.cur_token)
        return ast.IntegerLiteral(self.cur_token, int(self.cur_token.literal))

    def parse_boolean(self, depth) -> ast.Node:
        show_parse_info(depth, "BOOLEAN", self.cur_token)
        return ast.BooleanLiteral(
            self.cur_token,
            True if self.cur_token.token_type == TokenType.TRUE else False,
        )

    def parse_call_expression(
        self, left_expr: ast.Node, depth: int
    ) -> Union[ast.Node, ParseError]:
        show_parse_info(depth, "CALL EXPR", self.cur_token)
        cur_token = self.cur_token

        args_or_err = self.parse_list_of_expressions(TokenType.RParen, depth + 1)
        if isinstance(args_or_err, ParseError):
            return args_or_err

        return ast.CallExpression(cur_token, left_expr, args_or_err)

    def parse_function_literal(self, depth: int) -> Union[ast.Node, ParseError]:
        show_parse_info(depth, "FUNCTION", self.cur_token)
        cur_token = self.cur_token
        self.next_token()

        params_or_err = self.parse_list_of_expressions(TokenType.RParen, depth + 1)
        if isinstance(params_or_err, ParseError):
            return params_or_err

        self.expect_peek_and_advance(TokenType.LBrace)
        block_or_err = self.parse_block_statement(depth + 1)
        if isinstance(block_or_err, ParseError):
            return block_or_err

        return ast.Function(cur_token, params_or_err, block_or_err)

    def parse_list_of_expressions(
        self, closing_token: TokenType, depth: int
    ) -> Union[List[ast.Node], ParseError]:
        show_parse_info(depth, "LIST OF EXPR", self.cur_token)
        expressions: List[ast.Node] = []

        while (
            self.peek_token.token_type != closing_token
            and self.peek_token.token_type != TokenType.Eof
        ):
            self.next_token()
            expr_or_err = self.parse_expression(Precedence.Lowest, depth + 1)
            if isinstance(expr_or_err, ParseError):
                return expr_or_err

            expressions.append(expr_or_err)

            if self.peek_token.token_type == TokenType.Comma:
                self.next_token()

        self.expect_peek_and_advance(closing_token)
        return expressions

    def parse_if_expression(self, depth: int) -> Union[ast.Node, ParseError]:
        show_parse_info(depth, "IF EXPR", self.cur_token)
        cur_token = self.cur_token
        self.expect_peek_and_advance(TokenType.LParen)
        self.next_token()

        condition_or_err = self.parse_expression(Precedence.Lowest, depth + 1)
        if isinstance(condition_or_err, ParseError):
            return condition_or_err

        self.expect_peek_and_advance(TokenType.RParen)
        self.next_token()

        consequence_or_err = self.parse_block_statement(depth + 1)
        if isinstance(consequence_or_err, ParseError):
            return consequence_or_err

        self.next_token()

        if self.cur_token.token_type == TokenType.Else:
            self.next_token()
            alternative_or_err = self.parse_block_statement(depth + 1)
            if isinstance(alternative_or_err, ParseError):
                return alternative_or_err

            return ast.IfExpression(
                cur_token, condition_or_err, consequence_or_err, alternative_or_err
            )
        else:
            return ast.IfExpression(cur_token, condition_or_err, consequence_or_err)

    def parse_string_literal(self, depth: int) -> Union[ast.Node, ParseError]:
        show_parse_info(depth, "STRING LITERAL", self.cur_token)
        return ast.StringLiteral(self.cur_token, self.cur_token.literal)

    def parse_hash_literal(self, depth: int) -> Union[ast.Node, ParseError]:
        show_parse_info(depth, "HASH LITERAL", self.cur_token)
        cur_token = self.cur_token
        pairs: Dict[ast.Node, ast.Node] = {}

        def _parse_pair() -> Union[Tuple[ast.Node, ast.Node], ParseError]:
            left_or_err = self.parse_expression(Precedence.Lowest, depth + 1)
            if isinstance(left_or_err, ParseError):
                return left_or_err

            self.expect_peek_and_advance(TokenType.Colon)
            self.next_token()

            right_or_err = self.parse_expression(Precedence.Lowest, depth + 1)
            if isinstance(right_or_err, ParseError):
                return right_or_err

            self.next_token()
            return (left_or_err, right_or_err)

        while (
            self.peek_token.token_type != TokenType.RBrace
            and self.peek_token.token_type != TokenType.Eof
        ):
            self.next_token()
            pair_or_err = _parse_pair()
            if isinstance(pair_or_err, ParseError):
                return pair_or_err

            pairs[pair_or_err[0]] = pair_or_err[1]

        self.next_token()
        return ast.HashLiteral(cur_token, pairs)

    def parse_array_literal(self, depth: int) -> Union[ast.Node, ParseError]:
        show_parse_info(depth, "ARRAY LITERAL", self.cur_token)
        cur_token = self.cur_token

        exprs_or_err = self.parse_list_of_expressions(TokenType.RBracket, depth + 1)
        if isinstance(exprs_or_err, ParseError):
            return exprs_or_err

        return ast.ArrayLiteral(cur_token, exprs_or_err)

    def parse_index_expression(
        self, left_expr: ast.Node, depth: int
    ) -> Union[ast.Node, ParseError]:
        show_parse_info(depth, "INDEX EXPR", self.cur_token)
        cur_token = self.cur_token
        self.next_token()

        index_or_err = self.parse_expression(Precedence.Lowest, depth + 1)
        if isinstance(index_or_err, ParseError):
            return index_or_err

        self.expect_peek_and_advance(TokenType.RBracket)
        return ast.IndexExpression(cur_token, left_expr, index_or_err)

    def parse_grouped_expression(self, depth: int) -> Union[ast.Node, ParseError]:
        show_parse_info(depth, "GROUPED EXPR", self.cur_token)
        self.next_token()

        expr_or_err = self.parse_expression(Precedence.Lowest, depth + 1)
        if isinstance(expr_or_err, ParseError):
            return expr_or_err

        self.expect_peek_and_advance(TokenType.RParen)
        return expr_or_err

    def parse_prefix_expression(self, depth: int) -> Union[ast.Node, ParseError]:
        show_parse_info(depth, "PREFIX EXPR", self.cur_token)
        cur_tok = self.cur_token

        self.next_token()
        expr_or_error = self.parse_expression(Precedence.Prefix, depth + 1)
        if isinstance(expr_or_error, ParseError):
            return expr_or_error

        return ast.PrefixExpression(cur_tok, cur_tok.token_type.value, expr_or_error)

    def parse_infix_expression(
        self, left_expr: ast.Node, depth: int
    ) -> Union[ast.Node, ParseError]:
        show_parse_info(depth, "INFIX EXPR", self.cur_token)
        cur_token = self.cur_token
        cur_precedence = self.get_current_precendence()
        self.next_token()

        right_expr_or_error = self.parse_expression(cur_precedence, depth + 1)
        if isinstance(right_expr_or_error, ParseError):
            return right_expr_or_error

        return ast.InfixExpression(
            cur_token, left_expr, cur_token.token_type.value, right_expr_or_error
        )

    def parse_return_statement(self, depth: int) -> Union[ast.Node, ParseError]:
        show_parse_info(depth, "RETURN STMT", self.cur_token)
        cur_tok = self.cur_token
        self.next_token()
        expr_or_error = self.parse_expression(Precedence.Lowest, depth + 1)
        if isinstance(expr_or_error, ParseError):
            return expr_or_error

        self.maybe_remove_reduntant_semicolon()
        return ast.ReturnStatement(cur_tok, expr_or_error)

    def parse_let_statement(self, depth: int) -> Union[ast.Node, ParseError]:
        show_parse_info(depth, "LET STMT", self.cur_token)
        cur_tok = self.cur_token
        self.next_token()

        ident = self.parse_identifier(depth + 1)
        maybe_err = self.expect_peek_and_advance(TokenType.Assign)
        if maybe_err:
            return maybe_err

        self.next_token()
        expr_or_err = self.parse_expression(Precedence.Lowest, depth + 1)
        if isinstance(expr_or_err, ParseError):
            return expr_or_err

        self.maybe_remove_reduntant_semicolon()
        return ast.LetStatement(cur_tok, ident, expr_or_err)

    def parse_expression(
        self, precedence: Precedence, depth: int
    ) -> Union[ast.Node, ParseError]:
        cur_tok = self.cur_token

        prefix_fn = self.prefix_parse_functions.get(self.cur_token.token_type)
        if not prefix_fn:
            return ParseError(
                cur_tok.line,
                cur_tok.column,
                f"no prefix parse function found for '{self.cur_token.token_type}'",
            )

        left_expr_or_err = prefix_fn(depth)

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

            left_expr_or_err = infix_fn(left_expr_or_err, depth)

        return left_expr_or_err

    def parse_identifier(self, depth: int):
        show_parse_info(depth, "IDENTIFIER", self.cur_token)
        return ast.Identifier(self.cur_token, self.cur_token.literal)

    def maybe_remove_reduntant_semicolon(self):
        if self.peek_token.token_type == TokenType.Semicolon:
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


if __name__ == "__main__":
    input = """
        let x = fn(x, y) {
            if (x > y) {
                let x = x + 1
            } else {
                let y = y + 1
            }
            return x + y
        }
    """

    lexer = Lexer(input)
    parser = Parser(lexer)
    program = parser.parse_program()
    print(program)
