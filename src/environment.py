from dataclasses import dataclass
from typing import Dict, Optional

import object as obj


@dataclass
class Environment:
    def __init__(self, outer_env: Optional["Environment"] = None):
        self.outer = outer_env
        self.store: Dict[str, obj.Object] = {}

    def set(self, key: str, value: obj.Object) -> None:
        self.store[key] = value

    def get(self, key: str) -> obj.Object:
        res = self.store.get(key)
        if res is None and self.outer is None:
            return obj.NULL
        elif res is None:
            return self.outer.get(key)
        else:
            return res

    @staticmethod
    def create_enclosed_environment(outer_env: "Environment") -> "Environment":
        return Environment(outer_env)
