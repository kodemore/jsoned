from functools import partial

from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators.core_validators import ValidatorsMap
from jsoned.validators.number_validators import validate_minimum, validate_exclusive_minimum


class MinimumKeyword(AssertionKeyword):
    key = "minimum"

    def apply(self, document: JsonSchema, node: JsonObject, validator: ValidatorsMap):
        if node[self.key].type != JsonType.NUMBER:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.NUMBER)

        minimum = int(node[self.key])

        if "exclusiveMinimum" in node and bool(node["exclusiveMinimum"]) is True:
            validator[self.key] = partial(validate_exclusive_minimum, expected_minimum=minimum)
        else:
            validator[self.key] = partial(validate_minimum, expected_minimum=minimum)
