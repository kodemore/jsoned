from abc import abstractmethod
from decimal import Decimal
from functools import lru_cache
from typing import Sequence, Dict, overload, Protocol

from .json_pointer import JsonPointer
from .json_uri import JsonUri
from .types.json_array import JsonArray
from .types.json_boolean import JsonBoolean
from .types.json_null import JsonNull
from .types.json_number import JsonNumber
from .types.json_object import JsonObject
from .types.json_string import JsonString
from .types.json_type import JsonType
from .utils import AnyJsonType

__all__ = ["JsonDocument", "MetaJsonDocument", "JsonDocumentStore"]


class MetaJsonDocument(Protocol):
    @abstractmethod
    def init(self, document: "JsonDocument") -> None:
        ...


class JsonDocumentStore(Protocol):
    @abstractmethod
    def load(self, uri: JsonUri, meta: MetaJsonDocument) -> "JsonDocument":
        ...


class JsonDocument:
    def __init__(
        self,
        value: AnyJsonType,
        meta: MetaJsonDocument = None,
        store: JsonDocumentStore = None,
    ):
        self._json = value
        self._value = None
        self._ready = False

        if meta is None:
            from .meta_json_document import MetaJsonDocument as Meta

            self.meta = Meta.default()
        else:
            self.meta = meta

        if store is None:
            from .json_document_store import JsonDocumentStore as Store

            self.store = Store.default()
        else:
            self.store = store

    @property
    def value(self) -> JsonType:
        if self._ready:
            return self._value
        self._load()
        return self._value

    def _load(self) -> None:
        def _process_node(value: AnyJsonType, parent: JsonType = None) -> JsonType:
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
                node.value = [_process_node(item, node) for item in value]
                return node
            if isinstance(value, Dict) and all(isinstance(k, str) for k in value):
                node = JsonObject({}, parent)
                node.value = {
                    key: _process_node(value, node) for key, value in value.items()
                }
                return node

            raise TypeError(f"Passed value `{value=}` is not JSON-compatible.")

        self._value = _process_node(self._json)
        self.meta.init(self)
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

    def __repr__(self) -> str:
        return f"JsonDocument({self._json})"
