from collections import UserString

from .json_type import JsonType

__all__ = ["JsonString"]


class JsonString(JsonType):
    type = "string"

    def __contains__(self, char):
        if isinstance(char, UserString):
            char = char.data

        return char in self._value

    def __len__(self) -> int:
        return len(self._value)

    def __getitem__(self, index):
        return self._value[index]
