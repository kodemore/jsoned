from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema, LazyValidator
from jsoned.types import JsonObject, JsonType
from jsoned.validators.array_validators import ArrayValidator
from jsoned.validators.core_validators import CompoundValidator


class PrefixItemsKeyword(AssertionKeyword):
    key = "prefixItems"

    def apply(self, schema: JsonSchema, node: JsonObject, validator: CompoundValidator):
        if node[self.key].type != JsonType.ARRAY:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.ARRAY)

        if "items" in validator:
            array_validator = validator[self.key]
        else:
            array_validator = ArrayValidator()

        array_validator.prefix_items = [LazyValidator(schema, child_node) for child_node in node[self.key]]
        validator[self.key] = array_validator
