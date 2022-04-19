from collections import UserString

from .json_type import JsonType

__all__ = ["JsonString"]


class JsonString(JsonType, UserString):
    type = JsonType.STRING

    def __init__(self, value: str, parent: JsonType = None, key: str = ""):
        if not isinstance(value, str):
            raise TypeError(f"Expected str, got `{type(value)}` instead.")

        super().__init__(value, parent, key)

    @property
    def data(self) -> str:
        return self._value
