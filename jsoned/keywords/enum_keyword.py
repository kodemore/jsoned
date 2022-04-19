from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators.core_validators import EnumValidator, CompoundValidator


class EnumKeyword(AssertionKeyword):
    key = "enum"

    def apply(self, document: JsonSchema, node: JsonObject, validator: CompoundValidator) -> CompoundValidator:
        if node["enum"].type != JsonType.ARRAY:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.ARRAY)

        validator[self.key] = EnumValidator(expected_values=node["enum"].value, parent=validator)

        return validator
