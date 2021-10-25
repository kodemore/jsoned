from typing import Sequence
from collections import UserList

from .json_type import JsonType

__all__ = ["JsonArray"]


class JsonArray(JsonType):
    type = "array"

    def __len__(self) -> int:
        return len(self.value)

    def __getitem__(self, i):
        if isinstance(i, slice):
            return self.__class__(self.value[i])
        else:
            return self.value[i]

    def __setitem__(self, i, item):
        self.value[i] = item

    def __delitem__(self, i):
        del self.value[i]
