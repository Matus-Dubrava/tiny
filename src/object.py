from abc import ABC
from dataclasses import dataclass


class Object(ABC):
    def is_hashable(self) -> bool:
        raise NotImplementedError()


@dataclass
class IntegerObject(Object):
    value: int

    def __repr__(self):
        return f"{self.value}"

    def __hash__(self):
        return self.value

    def __eq__(self, other: "Object"):
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

    def __eq__(self, other: "Object"):
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

    def __eq__(self, other: "Object"):
        return self.value == other.value

    def is_hashable(self) -> bool:
        return True


@dataclass
class NullObject(Object):
    def __repr__(self):
        return "null"

    def __eq__(self, other: "NullObject"):
        return True

    def is_hashable(self) -> bool:
        return False


@dataclass
class ErrorObject(Object):
    value: str

    def __repr__(self):
        return f"ERROR: {self.value}"

    def __eq__(self, other: "ErrorObject"):
        return self.value == other.value

    def is_hashable(self) -> bool:
        return False


NULL = NullObject()
TRUE = BooleanObject(True)
FALSE = BooleanObject(False)
