from abc import ABC
from dataclasses import dataclass
from typing import List, Optional

from lexer import Token


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


@dataclass
class BlockStatement:
    token: Token
    statements: List[Node]

    def __repr__(self):
        return f"{{{'; '.join([f'{stmt}' for stmt in self.statements])}}}"


@dataclass
class Function(Node):
    token: Token
    paramters: List[Identifier]
    body: BlockStatement

    def __repr__(self):
        return f"fn({', '.join([f'{param}' for param in self.paramters])}) {self.body}"


@dataclass
class CallExpression(Node):
    token: Token
    func: Node  # can be either Function or Identifier
    arguments: List[Node]

    def __repr__(self):
        return f"{self.func}({', '.join([f'{arg}' for arg in self.arguments])})"


@dataclass
class IfExpression(Node):
    token: Token
    condition: Node
    consequence: Node
    alternative: Optional[Node] = None

    def __repr__(self):
        if self.alternative:
            return f"if ({self.condition}) {self.consequence} else {self.alternative}"
        else:
            return f"if ({self.condition}) {self.consequence}"


@dataclass
class ArrayLiteral(Node):
    token: Token
    expressions: List[Node]

    def __repr__(self):
        return f"[{', '.join([f'{expr}' for expr in self.expressions])}]"
