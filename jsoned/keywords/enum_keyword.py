from functools import partial

from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators.core_validators import ValidatorsMap
from jsoned.validators.core_validators import validate_enum


class EnumKeyword(AssertionKeyword):
    key = "enum"

    def apply(self, document: JsonSchema, node: JsonObject, validator: ValidatorsMap):
        if node["enum"].type != JsonType.ARRAY:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.ARRAY)

        validator[self.key] = partial(validate_enum, expected_values=node["enum"].value)
