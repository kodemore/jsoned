from functools import partial

from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators.core_validators import ValidatorsMap
from jsoned.validators.number_validators import validate_maximum, validate_exclusive_maximum


class MaximumKeyword(AssertionKeyword):
    key = "maximum"

    def apply(self, document: JsonSchema, node: JsonObject, validator: ValidatorsMap):
        if node[self.key].type != JsonType.NUMBER:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.NUMBER)

        maximum = int(node[self.key])

        if "exclusiveMaximum" in node and bool(node["exclusiveMaximum"]) is True:
            validator[self.key] = partial(validate_exclusive_maximum, expected_maximum=maximum)
        else:
            validator[self.key] = partial(validate_maximum, expected_maximum=maximum)
