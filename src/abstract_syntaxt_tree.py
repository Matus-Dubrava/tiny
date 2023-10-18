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


@dataclass
class BooleanLiteral(Node):
    token: Token
    value: bool


@dataclass
class Identifier(Node):
    token: Token
    name: str


@dataclass
class LetStatement(Node):
    token: Token
    ident: Identifier
    expr: Node


@dataclass
class ReturnStatement(Node):
    token: Token
    expr: Node


@dataclass
class DummyExpression(Node):
    token: Token = Token(0, 0, TokenType.Illegal)


@dataclass
class Program(Node):
    token: Token
    statements: List[Node]


@dataclass
class PrefixExpression(Node):
    token: Token
    operator: str
    expr: Node
