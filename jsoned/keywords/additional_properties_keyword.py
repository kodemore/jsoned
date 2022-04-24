from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema, LazyValidator
from jsoned.types import JsonObject, JsonType
from jsoned.validators.core_validators import CompoundValidator, FailValidator
from jsoned.validators.object_validators import ObjectValidator


class AdditionalPropertiesKeyword(AssertionKeyword):
    key = "additionalProperties"

    def apply(self, document: JsonSchema, node: JsonObject, validator: CompoundValidator):
        if node[self.key].type != JsonType.OBJECT and node[self.key].type != JsonType.BOOLEAN:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.OBJECT)

        if "properties" not in validator:
            validator["properties"] = ObjectValidator()

        if node[self.key].type == JsonType.BOOLEAN and node[self.key]:
            return  # additional properties are allowed

        # no additional properties should be present
        if node[self.key].type == JsonType.BOOLEAN:
            validator["properties"].additional_properties = FailValidator()
            return

        # nested validator for additional properties
        validator["properties"].additional_properties = LazyValidator(document, node[self.key])
