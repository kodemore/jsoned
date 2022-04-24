from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators.array_validators import ArrayUniqueValidators
from jsoned.validators.core_validators import CompoundValidator


class UniqueItemsKeyword(AssertionKeyword):
    key = "uniqueItems"

    def apply(self, schema: JsonSchema, node: JsonObject, validator: CompoundValidator):
        if node[self.key].type != JsonType.BOOLEAN:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.BOOLEAN)

        if not node[self.key]:
            return

        validator[self.key] = ArrayUniqueValidators()
