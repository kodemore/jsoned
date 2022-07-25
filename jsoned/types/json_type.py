from __future__ import annotations

from abc import ABC
from functools import cached_property
from typing import Optional

from jsoned.json_pointer import JsonPointer
from jsoned.utils import AnyJsonType

__all__ = ["JsonType", "JsonTypes"]


class JsonTypes:
    NULL = "null"
    OBJECT = "object"
    NUMBER = "number"
    BOOLEAN = "boolean"
    STRING = "string"
    ARRAY = "array"


class JsonType(ABC):
    _value: AnyJsonType
    parent: Optional[JsonType]
    type: JsonTypes
    key: str
    __slots__ = ["_value", "parent", "key", "type"]

    # consts
    NULL = JsonTypes.NULL
    OBJECT = JsonTypes.OBJECT
    NUMBER = JsonTypes.NUMBER
    BOOLEAN = JsonTypes.BOOLEAN
    STRING = JsonTypes.STRING
    ARRAY = JsonTypes.ARRAY

    def __init__(self, value, parent: JsonType = None, key: str = ""):
        self._value = value
        self.parent = parent
        self.key = key

    @property
    def value(self) -> AnyJsonType:
        return self._value

    @cached_property
    def path(self) -> JsonPointer:
        keys = []
        node = self
        while node.parent is not None:
            keys.append(node.key)
            node = node.parent

        keys.reverse()
        return JsonPointer.from_list(keys)

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
        return bool(self._value)

    def __repr__(self) -> str:
        return f"{self._value}"

    def is_root(self) -> bool:
        return self.parent is None

    @cached_property
    def root(self) -> JsonType:
        if self.is_root():
            return self

        return self.parent.root
