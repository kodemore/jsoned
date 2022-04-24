from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators.core_validators import CompoundValidator
from jsoned.validators.string_validators import StringMaximumLengthValidator


class MaximumLengthKeyword(AssertionKeyword):
    key = "maxLength"

    def apply(self, document: JsonSchema, node: JsonObject, validator: CompoundValidator):
        if node["maxLength"].type != JsonType.NUMBER:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.NUMBER)

        validator[self.key] = StringMaximumLengthValidator(expected_maximum=int(node[self.key]))
