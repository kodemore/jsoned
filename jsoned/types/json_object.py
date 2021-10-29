from typing import Dict, List
from typing import Set

from .json_type import JsonType

__all__ = ["JsonObject"]


class JsonObject(JsonType):
    type = "object"

    def __len__(self) -> int:
        return len(self._value)

    def __getitem__(self, key: str) -> JsonType:
        if key in self._value:
            return self._value[key]
        raise KeyError(key)

    def keys(self) -> Set[str]:
        return set(self._value.keys())

    def values(self) -> List[JsonType]:
        return list(self._value.values())

    def items(self):
        return self._value.items()

    def __setitem__(self, key: str, value: JsonType) -> None:
        if not isinstance(value, JsonType):
            raise ValueError(
                f"JsonObject expects only values of `JsonType` type, `{type(value)}` given instead."
            )

        if not isinstance(key, str):
            raise KeyError(key)

        self._value[key] = value

    def __iter__(self):
        return iter(self._value)
