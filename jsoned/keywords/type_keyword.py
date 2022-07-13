from functools import partial

from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators.core_validators import ValidatorsMap, AssertType
from jsoned.validators.core_validators import validate_type


class TypeKeyword(AssertionKeyword):
    key = "type"
    VALID_TYPES = [AssertType.STRING, AssertType.INTEGER, "number", "boolean", "array", "object", "null"]

    def apply(self, document: JsonSchema, node: JsonObject, validator: ValidatorsMap):
        valid_types = []

        if node[self.key].type == JsonType.STRING:
            try:
                valid_types.append(AssertType(str(node[self.key])))
            except ValueError:
                raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.STRING)
        elif node[self.key].type == JsonType.ARRAY:
            try:
                valid_types = [AssertType(str(item)) for item in node[self.key]]
            except ValueError:
                raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.STRING)
        else:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.STRING)

        validator[self.key] = partial(validate_type, expected_types=valid_types)
