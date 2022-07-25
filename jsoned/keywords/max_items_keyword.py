from functools import partial

from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators.array_validators import validate_array_length
from jsoned.validators.core_validators import ValidatorsMap


class MaximumItemsKeyword(AssertionKeyword):
    key = "maxItems"

    def apply(self, document: JsonSchema, node: JsonObject, validator: ValidatorsMap):
        if node[self.key].type != JsonType.NUMBER:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.NUMBER)

        if "array_length" in validator:
            child_validator = validator["array_length"]
            child_validator = partial(child_validator, expected_maximum=int(node[self.key]))
        else:
            child_validator = partial(validate_array_length, expected_maximum=int(node[self.key]))

        validator["array_length"] = child_validator
