from abc import ABC
from dataclasses import dataclass
from typing import List
import abstract_syntaxt_tree as ast
from typing import Optional, Dict


class Object(ABC):
    def is_hashable(self) -> bool:
        raise NotImplementedError()


@dataclass
class Environment:
    def __init__(self, outer_env: Optional["Environment"] = None):
        self.outer = outer_env
        self.store: Dict[str, Object] = {}

    def set(self, key: str, value: Object) -> None:
        self.store[key] = value

    def get(self, key: str) -> Object:
        res = self.store.get(key)
        if res is None and self.outer is None:
            return NULL
        elif res is None:
            return self.outer.get(key)
        else:
            return res

    @staticmethod
    def create_enclosed_environment(outer_env: "Environment") -> "Environment":
        return Environment(outer_env)


@dataclass
class IntegerObject(Object):
    value: int

    def __repr__(self):
        return f"{self.value}"

    def __hash__(self):
        return self.value

    def __eq__(self, other):
        return self.value == other.value

    def is_hashable(self) -> bool:
        return True


@dataclass
class StringObject(Object):
    value: str

    def __repr__(self):
        return self.value

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def is_hashable(self) -> bool:
        return True


@dataclass
class BooleanObject(Object):
    value: bool

    def __repr__(self):
        return f"{self.value}"

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def is_hashable(self) -> bool:
        return True


@dataclass
class NullObject(Object):
    def __repr__(self):
        return "null"

    def __eq__(self, other):
        return True

    def is_hashable(self) -> bool:
        return False


@dataclass
class ErrorObject(Object):
    value: str

    def __repr__(self):
        return f"ERROR: {self.value}"

    def __eq__(self, other):
        return self.value == other.value

    def is_hashable(self) -> bool:
        return False


@dataclass
class ReturnObject(Object):
    value: Object

    def __repr__(self):
        return f"return {self.value}"

    def __eq__(self, other):
        return self.value == other.value

    def is_hashable(self) -> bool:
        return False


@dataclass
class FunctionObject(Object):
    arguments: List[ast.Identifier]
    body: ast.BlockStatement
    env: Environment

    def __repr__(self):
        return f"fn({','.join([f'{arg}' for arg in self.arguments])}) {{{self.body}}}"

    def __eq__(self, other):
        return self == other

    def is_hashable(self) -> bool:
        return False


NULL = NullObject()
TRUE = BooleanObject(True)
FALSE = BooleanObject(False)
