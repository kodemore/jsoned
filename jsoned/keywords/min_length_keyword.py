from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema, CompoundValidator
from jsoned.types import JsonObject, JsonType
from jsoned.validators.string_validators import StringMinimumLengthValidator


class MinimumLengthKeyword(AssertionKeyword):
    key = "minLength"

    def apply(self, document: JsonSchema, node: JsonObject, validator: CompoundValidator) -> CompoundValidator:
        if node[self.key].type != JsonType.NUMBER:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.NUMBER)

        validator[self.key] = StringMinimumLengthValidator(expected_minimum=int(node[self.key]), parent=validator)

        return validator
