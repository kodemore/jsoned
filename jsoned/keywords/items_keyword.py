from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema, LazyValidator
from jsoned.types import JsonObject, JsonType
from jsoned.validators.array_validators import ArrayValidator
from jsoned.validators.core_validators import CompoundValidator


class ItemsKeyword(AssertionKeyword):
    key = "items"

    def apply(self, schema: JsonSchema, node: JsonObject, validator: CompoundValidator):
        if node[self.key].type in [JsonType.STRING, JsonType.NULL, JsonType.NUMBER]:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.OBJECT)

        if self.key in validator:
            array_validator = validator[self.key]
        else:
            array_validator = ArrayValidator()

        if node[self.key].type == JsonType.ARRAY:
            array_validator.prefix_items = [LazyValidator(schema, child_node) for child_node in node[self.key]]

            if "additionalItems" in node and (node["additionalItems"].type != JsonType.BOOLEAN or not node["additionalItems"]):
                array_validator.items = LazyValidator(schema, node["additionalItems"])
        else:
            if node[self.key].type != JsonType.BOOLEAN or not node[self.key]:
                array_validator.items = LazyValidator(schema, node[self.key])

        validator[self.key] = array_validator
