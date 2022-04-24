from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators.core_validators import CompoundValidator
from jsoned.validators.core_validators import TypeValidator


class TypeKeyword(AssertionKeyword):
    key = "type"
    VALID_TYPES = ["string", "integer", "number", "boolean", "array", "object", "null"]

    def apply(self, document: JsonSchema, node: JsonObject, validator: CompoundValidator):
        valid_types = []

        if node[self.key].type == JsonType.STRING:
            valid_types.append(str(node[self.key]))
        elif node[self.key].type == JsonType.ARRAY:
            valid_types = [str(item) for item in node[self.key]]
        else:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.STRING)

        for i in valid_types:
            if i not in self.VALID_TYPES:
                raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.STRING)

        validator[self.key] = TypeValidator(expected_types=valid_types)
