from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema, CompoundValidator
from jsoned.types import JsonObject, JsonType
from jsoned.validators.number_validators import NumberMultipleOfValidator


class MultipleOfKeyword(AssertionKeyword):
    key = "multipleOf"

    def apply(self, document: JsonSchema, node: JsonObject, validator: CompoundValidator) -> CompoundValidator:
        if node[self.key].type != JsonType.NUMBER:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.NUMBER)

        validator[self.key] = NumberMultipleOfValidator(multiple_of=node[self.key].value, parent=validator)

        return validator
