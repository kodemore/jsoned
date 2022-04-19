from functools import cached_property
from typing import Set, List

from jsoned.json_core import ApplicatorKeyword, JsonSchema
from jsoned.json_pointer import JsonPointer
from jsoned.json_store import JsonStore
from jsoned.types.json_complex import JsonObject
from jsoned.types.json_type import JsonType
from jsoned.uri import Uri

__all__ = ["JsonReference", "RefKeyword"]


class JsonReference(JsonType):

    def __init__(self, uri: Uri, node: JsonObject, document: JsonSchema, pointer: JsonPointer):
        self.uri = uri
        self.node = node
        self.schema = document
        self.pointer = pointer
        self.key = node.key

    @property
    def type(self) -> str:
        return self.fragment.type

    @cached_property
    def parent(self) -> JsonType:
        return self.node.parent

    @cached_property
    def fragment(self) -> JsonType:
        return self.schema.query(self.pointer)

    @property
    def _value(self):
        if not self.schema.ready:
            return self.node._value
        else:
            return self._ref_value

    @cached_property
    def _ref_value(self):
        fragment = self.fragment
        if fragment.type != JsonType.OBJECT:
            return fragment

        result = {}

        for key, value in self.node.items():
            if key == "$ref":
                continue
            result[key] = value

        for key, value in self.fragment.items():
            result[key] = value

        return result

    def __contains__(self, key):
        return key in self._value

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

    def __repr__(self) -> str:
        return f"JsonReference({self.uri})"


class RefKeyword(ApplicatorKeyword):
    key: str = "$ref"

    def __init__(self, store: JsonStore):
        self.store = store

    def apply(self, document: JsonSchema, node: JsonObject) -> JsonType:
        uri = Uri(str(node["$ref"]))
        pointer = JsonPointer(uri.fragment)

        if not uri.base_uri:  # reference to self document
            return JsonReference(uri, node, document, pointer)

        referenced_document = self.store.load(uri, document.vocabulary)
        return JsonReference(uri, node, referenced_document, pointer)
