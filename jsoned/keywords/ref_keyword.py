from functools import cached_property

from jsoned.json_core import JsonDocument
from jsoned.json_pointer import JsonPointer
from jsoned.json_uri import JsonUri
from jsoned.types.json_object import JsonObject
from jsoned.types.json_type import JsonType

__all__ = ["JsonReference", "RefKeyword"]


class JsonReference(JsonType):
    type = "reference"

    def __init__(self, node: JsonObject, document: JsonDocument, pointer: JsonPointer):
        self.document = document
        self.parent = node.parent
        self.node = node
        self._value = None
        self.pointer = pointer

    @cached_property
    def value(self):
        result = {}
        for key, value in self.node.items():
            if key == "$ref":
                continue
            result[key] = value

        fragment = self.document.query(self.pointer)
        for key, value in fragment.items():
            result[key] = value

        return result


class RefKeyword:
    key: str = "$ref"

    @staticmethod
    def resolve(document: JsonDocument, node: JsonObject) -> JsonType:
        uri = JsonUri(str(node["$ref"]))
        pointer = JsonPointer(uri.fragment)

        if not uri.base_uri:  # reference to self document
            return JsonReference(node, document, pointer)

        referenced_document = document.store.load(uri, document.meta)

        return JsonReference(node, referenced_document, pointer)
