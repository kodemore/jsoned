from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema, CompoundValidator
from jsoned.types import JsonObject, JsonType
from jsoned.validators.string_validators import StringPatternValidator


class PatternKeyword(AssertionKeyword):
    key = "pattern"

    def apply(self, document: JsonSchema, node: JsonObject, validator: CompoundValidator) -> CompoundValidator:
        if node[self.key].type != JsonType.STRING:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.STRING)

        pattern = str(node[self.key])

        validator[self.key] = StringPatternValidator(pattern=pattern, parent=validator)

        return validator
