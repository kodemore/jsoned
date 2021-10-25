from typing import overload

from .json_type import JsonType

__all__ = ["JsonBoolean"]


class JsonBoolean(JsonType):
    type = "boolean"

    @overload
    def __eq__(self, other: "JsonBoolean") -> bool:
        ...

    @overload
    def __eq__(self, other: bool) -> bool:
        ...

    def __eq__(self, other) -> bool:
        if isinstance(other, JsonBoolean):
            return self.value == other.value
        if isinstance(other, bool):
            return self.value == other

        raise TypeError(f"Expected bool or JsonBoolean, got `{type(other)}` instead.")
