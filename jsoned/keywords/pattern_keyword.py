from functools import partial

from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators.core_validators import ValidatorsMap
from jsoned.validators.string_validators import validate_string_pattern


class PatternKeyword(AssertionKeyword):
    key = "pattern"

    def apply(self, document: JsonSchema, node: JsonObject, validator: ValidatorsMap):
        if node[self.key].type != JsonType.STRING:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.STRING)

        pattern = str(node[self.key])

        validator[self.key] = partial(validate_string_pattern, expected_pattern=pattern)
