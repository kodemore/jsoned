from __future__ import annotations

__all__ = ["SchemaParseError"]

from jsoned.json_pointer import JsonPointer
from jsoned.types.json_complex import JsonObject
from jsoned.types.json_type import JsonTypes


class SchemaParseError(RuntimeError):
    path: JsonPointer

    def __init__(self, msg: str, path: JsonPointer):
        self.path = path
        super().__init__(msg)

    @classmethod
    def for_invalid_keyword_value(cls, node: JsonObject, keyword: str, expected_type: JsonTypes) -> 'SchemaParseError':
        message = f"Parsing failed at `{node.path}`. Passed document is not a valid json schema object. "
        f"`{keyword}` property has invalid type `{node[keyword].type}`, expected `{expected_type}` type."

        return cls(message, node.path)

    @classmethod
    def for_keyword_missing_dependency(cls, node: JsonObject, keyword: str, depends_on: str) -> 'SchemaParseError':
        message = f"Parsing failed at `{node.path}`. Passed document is not a valid json schema object. "
        f"`{keyword}` property depends on `{depends_on}` property to be present."

        return cls(message, node.path)
