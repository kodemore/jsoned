from typing import Dict, List
from typing import Set

from .json_type import JsonType

__all__ = ["JsonObject"]


class JsonObject(JsonType):
    type = "object"

    def __len__(self) -> int:
        return len(self.value)

    def __getitem__(self, key: str) -> JsonType:
        if key in self.value:
            return self.value[key]
        raise KeyError(key)

    def keys(self) -> Set[str]:
        return set(self.value.keys())

    def values(self) -> List[JsonType]:
        return list(self.value.values())

    def items(self):
        return self.value.items()

    def __setitem__(self, key: str, value: JsonType) -> None:
        if not isinstance(value, JsonType):
            raise ValueError(
                f"JsonObject expects only values of `JsonType` type, `{type(value)}` given instead."
            )

        if not isinstance(key, str):
            raise KeyError(key)

        self.value[key] = value

    def __iter__(self):
        return iter(self.value)
