from functools import cached_property
from typing import Set, List

from jsoned.json_pointer import JsonPointer
from jsoned.uri import Uri
from jsoned.json_core import Keyword, JsonDocument, JsonLoader
from jsoned.types.json_object import JsonObject
from jsoned.types.json_type import JsonType

__all__ = ["JsonReference", "RefKeyword"]


class JsonReference(JsonType):
    type = "reference"

    def __init__(self, uri: Uri, node: JsonObject, document: JsonDocument, pointer: JsonPointer):
        self.uri = uri
        self.node = node
        self.document = document
        self.pointer = pointer

    @cached_property
    def parent(self) -> JsonType:
        return self.node.parent

    @cached_property
    def fragment(self) -> JsonType:
        return self.document.query(self.pointer)

    @cached_property
    def _value(self):
        fragment = self.fragment
        if not isinstance(fragment, JsonObject):
            return fragment

        result = {}
        for key, value in self.node.items():
            if key == "$ref":
                continue
            result[key] = value

        for key, value in self.fragment.items():
            result[key] = value

        return result

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


class RefKeyword(Keyword):
    key: str = "$ref"

    def __init__(self, loader: JsonLoader):
        self.loader = loader

    def resolve(self, document: JsonDocument, node: JsonObject) -> JsonType:
        uri = Uri(str(node["$ref"]))
        pointer = JsonPointer(uri.fragment)

        if not uri.base_uri:  # reference to self document
            return JsonReference(uri, node, document, pointer)

        referenced_document = self.loader.load(uri)
        return JsonReference(uri, node, referenced_document, pointer)
