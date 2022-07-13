from functools import partial

from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators.core_validators import ValidatorsMap, validate_const


class ConstKeyword(AssertionKeyword):
    key = "const"

    def apply(self, document: JsonSchema, node: JsonObject, validator: ValidatorsMap):
        if node[self.key].type == JsonType.ARRAY or node[self.key].type == JsonType.OBJECT:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.STRING)

        validator[self.key] = partial(validate_const, expected_value=node[self.key].value)
