from abc import ABC

from jsoned.utils import AnyJsonType

__all__ = ["JsonType"]


class JsonType(ABC):
    __slots__ = ["type", "value", "parent"]
    type: str
    value: AnyJsonType
    parent: "JsonType"

    def __init__(self, value, parent: "JsonType" = None):
        self.value = value
        self.parent = parent

    def __eq__(self, other):
        if isinstance(other, JsonType):
            return self.value == other.value
        else:
            return self.value == other

    def __lt__(self, other):
        if isinstance(other, JsonType):
            return self.value < other.value
        else:
            return self.value < other

    def __le__(self, other):
        if isinstance(other, JsonType):
            return self.value <= other.value
        else:
            return self.value <= other

    def __gt__(self, other):
        if isinstance(other, JsonType):
            return self.value > other.value
        else:
            return self.value > other

    def __ge__(self, other):
        if isinstance(other, JsonType):
            return self.value >= other.value
        else:
            return self.value >= other

    def __bool__(self) -> bool:
        return self.value

    def __repr__(self) -> str:
        return f"{self.value}"
