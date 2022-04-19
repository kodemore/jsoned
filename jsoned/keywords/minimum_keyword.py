from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema, CompoundValidator
from jsoned.types import JsonObject, JsonType
from jsoned.validators.number_validators import NumberMinimumValidator


class MinimumKeyword(AssertionKeyword):
    key = "minimum"

    def apply(self, document: JsonSchema, node: JsonObject, validator: CompoundValidator) -> CompoundValidator:
        if node[self.key].type != JsonType.NUMBER:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.NUMBER)

        minimum = node[self.key].value

        if "exclusiveMinimum" in node and node["exclusiveMinimum"] == True:
            validator[self.key] = NumberMinimumValidator(expected_minimum=minimum, exclusive=True, parent=validator)
        else:
            validator[self.key] = NumberMinimumValidator(expected_minimum=minimum, parent=validator)

        return validator
