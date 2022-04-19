from decimal import Decimal
from typing import List, MutableMapping, Iterable, Mapping, Any

from jsoned.types.json_number import JsonNumber
from jsoned.types.json_string import JsonString
from . import JsonBoolean, JsonNull
from .json_type import JsonType

__all__ = ["JsonArray", "JsonObject"]


class JsonObject(JsonType, MutableMapping):
    type = JsonType.OBJECT

    def __init__(self, value: Mapping, parent: JsonType = None, key: str = ""):
        value = {key: _map_value(item, self, key) for key, item in value.items()}
        super().__init__(value, parent, key)

    def __len__(self) -> int:
        return len(self._value)

    def __getitem__(self, key: str) -> JsonType:
        if key in self._value:
            return self._value[key]
        raise KeyError(key)

    def keys(self) -> List[str]:
        return list(self._value.keys())

    def values(self) -> List[JsonType]:
        return list(self._value.values())

    def items(self):
        return self._value.items()

    def __setitem__(self, key: str, value: Any) -> None:
        if not isinstance(key, str):
            raise KeyError(key)

        self._value[key] = _map_value(value, self, key)

    def __delitem__(self, key: str) -> None:
        if key not in self:
            return

        del self._value[key]

    def __contains__(self, key: str) -> bool:
        return key in self._value

    def __iter__(self):
        return iter(self._value)


class JsonArray(JsonType, Iterable):
    type = JsonType.ARRAY

    def __init__(self, value: Iterable, parent: JsonType = None, key: str = ""):
        value = [_map_value(item, self, str(key)) for key, item in enumerate(value)]
        super().__init__(value, parent, key)

    def __len__(self) -> int:
        return len(self._value)

    def __getitem__(self, i):
        if isinstance(i, slice):
            return self.__class__(self._value[i])
        else:
            return self._value[i]

    def __setitem__(self, i, item):
        self._value[i] = item

    def __delitem__(self, i):
        del self._value[i]

    def __contains__(self, item) -> bool:
        return item in self._value

    def __iter__(self):
        return iter(self._value)


_class_map = {
    int: JsonNumber,
    float: JsonNumber,
    Decimal: JsonNumber,
    str: JsonString,
    Iterable: JsonArray,
    Mapping: JsonObject,
}


def _map_value(value: Any, parent: JsonType = None, key: str = "") -> JsonType:

    if isinstance(value, JsonType):
        return value

    if isinstance(value, Mapping):
        return JsonObject(value, parent, key)

    if isinstance(value, str):
        return JsonString(value, parent, key)

    if isinstance(value, bool):
        return JsonBoolean(value, parent, key)

    if isinstance(value, Iterable):
        return JsonArray(value, parent, key)

    if isinstance(value, (int, float, Decimal)):
        return JsonNumber(value, parent, key)

    if value is None:
        return JsonNull(None, parent, key)

    raise ValueError(f"Cannot map value {value=}")
