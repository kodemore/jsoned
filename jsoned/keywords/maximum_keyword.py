from functools import partial

from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema, CompoundValidator
from jsoned.types import JsonObject, JsonType
from jsoned.validators.number_validators import NumberMaximumValidator


class MaximumKeyword(AssertionKeyword):
    key = "maximum"

    def apply(self, document: JsonSchema, node: JsonObject, validator: CompoundValidator) -> CompoundValidator:
        if node[self.key].type != JsonType.NUMBER:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.NUMBER)

        maximum = node[self.key].value

        if "exclusiveMaximum" in node and node["exclusiveMaximum"] == True:
            validator[self.key] = NumberMaximumValidator(expected_maximum=maximum, exclusive=True, parent=validator)
        else:
            validator[self.key] = NumberMaximumValidator(expected_maximum=maximum, parent=validator)

        return validator
