from abc import ABC
from dataclasses import dataclass
from lexer import Token


class Node(ABC):
    pass


@dataclass
class IntegerLiteral(Node):
    token: Token
    value: int


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
