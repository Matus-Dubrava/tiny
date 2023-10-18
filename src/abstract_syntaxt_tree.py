from abc import ABC
from dataclasses import dataclass
from typing import List

from lexer import Token, TokenType


class Node(ABC):
    pass


@dataclass
class IntegerLiteral(Node):
    token: Token
    value: int

    def __repr__(self):
        return f"{self.value}"


@dataclass
class BooleanLiteral(Node):
    token: Token
    value: bool

    def __repr__(self):
        return f"{self.value}"


@dataclass
class Identifier(Node):
    token: Token
    name: str

    def __repr__(self):
        return self.name


@dataclass
class LetStatement(Node):
    token: Token
    ident: Identifier
    expr: Node

    def __repr__(self):
        return f"let {self.ident} = {self.expr}"


@dataclass
class ReturnStatement(Node):
    token: Token
    expr: Node

    def __repr__(self):
        return f"return {self.expr}"


@dataclass
class Program(Node):
    token: Token
    statements: List[Node]

    def __repr__(self):
        return "; ".join([f"{stmt}" for stmt in self.statements])


@dataclass
class PrefixExpression(Node):
    token: Token
    operator: str
    expr: Node

    def __repr__(self):
        return f"({self.operator}{self.expr})"


@dataclass
class InfixExpression(Node):
    token: Token
    left_expr: Node
    operator: str
    right_expr: Node

    def __repr__(self):
        return f"({self.left_expr} {self.operator} {self.right_expr})"
