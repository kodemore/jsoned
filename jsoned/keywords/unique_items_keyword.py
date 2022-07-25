from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators.array_validators import validate_array_unique
from jsoned.validators.core_validators import ValidatorsMap


class UniqueItemsKeyword(AssertionKeyword):
    key = "uniqueItems"

    def apply(self, schema: JsonSchema, node: JsonObject, validator: ValidatorsMap):
        if node[self.key].type != JsonType.BOOLEAN:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.BOOLEAN)

        if not node[self.key]:
            return

        validator[self.key] = validate_array_unique
