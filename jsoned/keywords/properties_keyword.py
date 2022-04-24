from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema, LazyValidator
from jsoned.types import JsonObject, JsonType
from jsoned.validators.core_validators import CompoundValidator
from jsoned.validators.object_validators import PropertiesValidator


class PropertiesKeyword(AssertionKeyword):
    key = "properties"

    def apply(self, schema: JsonSchema, node: JsonObject, validator: CompoundValidator):
        if node[self.key].type != JsonType.OBJECT:
            raise SchemaParseError.for_invalid_keyword_value(node, "properties", JsonType.OBJECT)

        if self.key in validator:
            properties_validator = validator[self.key]
        else:
            properties_validator = PropertiesValidator()

        for key, child_node in node[self.key].items():
            properties_validator[key] = LazyValidator(schema, child_node)

        validator[self.key] = properties_validator
