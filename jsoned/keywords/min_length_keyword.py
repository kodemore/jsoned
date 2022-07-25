from functools import partial

from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators.core_validators import ValidatorsMap
from jsoned.validators.string_validators import validate_string_length


class MinimumLengthKeyword(AssertionKeyword):
    key = "minLength"

    def apply(self, document: JsonSchema, node: JsonObject, validator: ValidatorsMap):
        if node[self.key].type != JsonType.NUMBER:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.NUMBER)

        if "string_length" in validator:
            child_validator = validator["string_length"]
            child_validator = partial(child_validator, expected_minimum=int(node[self.key]))
        else:
            child_validator = partial(validate_string_length, expected_minimum=int(node[self.key]))

        validator["string_length"] = child_validator
