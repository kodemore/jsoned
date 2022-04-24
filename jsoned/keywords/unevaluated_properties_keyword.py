from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators.core_validators import CompoundValidator, FailValidator
from jsoned.validators.object_validators import PropertiesValidator


class UnevaluatedPropertiesKeyword(AssertionKeyword):
    key = "unevaluatedProperties"

    def apply(self, document: JsonSchema, node: JsonObject, validator: CompoundValidator):
        if node[self.key].type != JsonType.BOOLEAN:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.BOOLEAN)

        if "properties" not in validator:
            validator["properties"] = PropertiesValidator()

        if node[self.key].type == JsonType.BOOLEAN and node[self.key]:
            return  # additional properties are allowed

        validator["properties"].unevaluated_properties = FailValidator()
