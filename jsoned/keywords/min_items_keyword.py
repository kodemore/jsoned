from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators.array_validators import ArrayMinimumLengthValidator
from jsoned.validators.core_validators import CompoundValidator


class MinimumItemsKeyword(AssertionKeyword):
    key = "minItems"

    def apply(self, document: JsonSchema, node: JsonObject, validator: CompoundValidator):
        if node[self.key].type != JsonType.NUMBER:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.NUMBER)

        validator[self.key] = ArrayMinimumLengthValidator(expected_minimum=int(node[self.key]))
