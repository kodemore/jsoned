from abc import ABC

from jsoned.utils import AnyJsonType

__all__ = ["JsonType"]


class JsonType(ABC):
    __slots__ = ["type", "_value", "parent"]
    type: str
    _value: AnyJsonType
    parent: "JsonType"

    def __init__(self, value, parent: "JsonType" = None):
        self._value = value
        self.parent = parent

    @property
    def value(self) -> AnyJsonType:
        return self._value

    def __eq__(self, other):
        if isinstance(other, JsonType):
            return self._value == other._value
        else:
            return self._value == other

    def __lt__(self, other):
        if isinstance(other, JsonType):
            return self._value < other._value
        else:
            return self._value < other

    def __le__(self, other):
        if isinstance(other, JsonType):
            return self._value <= other._value
        else:
            return self._value <= other

    def __gt__(self, other):
        if isinstance(other, JsonType):
            return self._value > other._value
        else:
            return self._value > other

    def __ge__(self, other):
        if isinstance(other, JsonType):
            return self._value >= other._value
        else:
            return self._value >= other

    def __bool__(self) -> bool:
        return self._value

    def __repr__(self) -> str:
        return f"{self._value}"
