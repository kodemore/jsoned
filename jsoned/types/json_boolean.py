from __future__ import annotations

from typing import overload

from .json_type import JsonType

__all__ = ["JsonBoolean"]


class JsonBoolean(JsonType):
    type = JsonType.BOOLEAN

    def __init__(self, value: bool, parent: JsonType = None, key: str = ""):
        if not isinstance(value, bool):
            raise TypeError(f"Expected bool, got `{type(value)}` instead.")

        super().__init__(value, parent, key)

    @overload
    def __eq__(self, other: JsonBoolean) -> bool:
        ...

    @overload
    def __eq__(self, other: bool) -> bool:
        ...

    def __eq__(self, other) -> bool:
        if isinstance(other, JsonBoolean):
            return self._value == other._value
        if isinstance(other, bool):
            return self._value == other

        raise TypeError(f"Expected bool or JsonBoolean, got `{type(other)}` instead.")

    def __repr__(self) -> str:
        return f"JsonBool({self._value})"
