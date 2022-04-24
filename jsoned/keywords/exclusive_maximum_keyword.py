from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators.core_validators import CompoundValidator
from jsoned.validators.number_validators import NumberMaximumValidator


class ExclusiveMaximumKeyword(AssertionKeyword):
    key = "exclusiveMaximum"

    def apply(self, document: JsonSchema, node: JsonObject, validator: CompoundValidator):
        if node[self.key].type == JsonType.BOOLEAN:
            if "maximum" in node:
                return validator
            else:
                raise SchemaParseError.for_keyword_missing_dependency(node, self.key, "maximum")

        if node[self.key].type != JsonType.NUMBER:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.NUMBER)

        validator[self.key] = NumberMaximumValidator(expected_maximum=node[self.key].value, exclusive=True)
