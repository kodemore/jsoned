from __future__ import annotations

from abc import ABC, abstractmethod
from decimal import Decimal
from functools import lru_cache
from typing import List, Type
from typing import Sequence, Dict, overload

from .json_pointer import JsonPointer
from .types.json_array import JsonArray
from .types.json_boolean import JsonBoolean
from .types.json_null import JsonNull
from .types.json_number import JsonNumber
from .types.json_object import JsonObject
from .types.json_string import JsonString
from .types.json_type import JsonType
from .uri import Uri
from .utils import AnyJsonType

__all__ = ["JsonDocument", "Keyword", "JsonLoader"]


class Keyword(ABC):
    key: str
    dependencies: List[Keyword]

    @abstractmethod
    def resolve(self, document: JsonDocument, node: JsonType) -> JsonType:
        ...


class JsonLoader(ABC):
    @abstractmethod
    def load(self, uri: Uri) -> JsonDocument:
        ...


class JsonDocument:
    def __init__(self, value: AnyJsonType, keywords: List[Keyword] = None):
        self._json = value
        self._value = None
        self._ready = False
        self._keywords = keywords if keywords is not None else []
        self.anchors: Dict[str, JsonType] = {}
        self.src = None
        self.uri = None

    @property
    def value(self) -> JsonType:
        if self._ready:
            return self._value
        self._load()
        return self._value

    def _load(self) -> None:
        self._value = self._process_node(self._json)
        self._ready = True

    @overload
    def query(self, query: str) -> JsonType:
        ...

    @overload
    def query(self, pointer: JsonPointer) -> JsonType:
        ...

    @lru_cache()
    def query(self, query) -> JsonType:
        if isinstance(query, str):
            pointer = JsonPointer(query)
        elif isinstance(query, JsonPointer):
            pointer = query
        else:
            raise ValueError(
                f"Query must be either `str` or `JsonPointer`, `{type(query)}` given instead."
            )
        node = self.value

        if len(pointer) == 1 and pointer[0] in self.anchors:
            return self.anchors[pointer[0]]

        visited = []
        for key in pointer:
            if isinstance(node, JsonArray):
                node = node[int(key)]
            elif isinstance(node, JsonObject):
                node = node[key]
            else:
                raise KeyError(
                    f"Could not resolve `{key}` in reference `{pointer}` at `{JsonPointer.from_list(visited)}`"
                )

            visited.append(key)
        return node

    def _process_node(self, value: AnyJsonType, parent: JsonType = None) -> JsonType:
        if value is None:
            return JsonNull(None, parent)
        if isinstance(value, bool):
            return JsonBoolean(value, parent)
        if isinstance(value, (int, Decimal, float)):
            return JsonNumber(value, parent)
        if isinstance(value, str):
            return JsonString(value, parent)
        if isinstance(value, Sequence):
            node = JsonArray([], parent)
            node._value = [self._process_node(item, node) for item in value]
            return node
        if isinstance(value, Dict) and all(isinstance(k, str) for k in value):
            node = JsonObject({}, parent)
            node._value = {
                key: self._process_node(value, node) for key, value in value.items()
            }
            for keyword in self._keywords:
                if keyword.key not in value:
                    continue
                node = keyword.resolve(self, node)
            return node

        raise TypeError(f"Passed value `{value=}` is not JSON-compatible.")

    def __repr__(self) -> str:
        return f"JsonDocument({self.value})"
