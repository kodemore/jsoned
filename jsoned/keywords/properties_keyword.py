from typing import Dict, Any

from jsoned.errors import TypeValidationError
from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema, CompoundValidator, build_validator_for_node
from jsoned.types import JsonObject, JsonType
from jsoned.validators import Validator


class PropertiesValidator(CompoundValidator):
    def __init__(self, schema: JsonSchema, node: JsonObject, parent: Validator):
        self._node = node
        self._schema = schema
        super().__init__(key="", parent=parent)

    def validate(self, value: Dict[str, Any]):
        if not isinstance(value, dict):
            raise TypeValidationError(path=self.path, expected_types=["object"])

        for key in self._node.keys():
            if key not in value:
                continue

            if key not in self:
                self[key] = build_validator_for_node(
                    self._schema,
                    self._node[key],
                    CompoundValidator(key=f".{key}", parent=self)
                )

            self[key](value[key])


class PropertiesKeyword(AssertionKeyword):
    key = "properties"

    def apply(self, document: JsonSchema, node: JsonObject, validator: CompoundValidator) -> CompoundValidator:
        if node[self.key].type != JsonType.OBJECT:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.OBJECT)

        validator[self.key] = PropertiesValidator(document, node[self.key], parent=validator)

        return validator
