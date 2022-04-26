from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators.core_validators import CompoundValidator
from jsoned.validators.object_validators import RequiredPropertiesValidator


class RequiredPropertiesKeyword(AssertionKeyword):
    key = "required"

    def apply(self, document: JsonSchema, node: JsonObject, validator: CompoundValidator):
        if node[self.key].type != JsonType.ARRAY:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.ARRAY)

        validator[self.key] = RequiredPropertiesValidator([str(item) for item in node[self.key]])
