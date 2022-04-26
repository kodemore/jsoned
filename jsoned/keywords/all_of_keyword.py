from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema, LazyValidator
from jsoned.types import JsonObject, JsonType
from jsoned.validators import CompoundValidator
from jsoned.validators.composition_validators import AllOfValidator


class AllOfKeyword(AssertionKeyword):
    key = "allOf"

    def apply(self, document: JsonSchema, node: JsonObject, validator: CompoundValidator):
        if node[self.key].type != JsonType.ARRAY:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.ARRAY)

        child_validator = AllOfValidator()
        for child_node in node[self.key]:
            child_validator.validators.append(LazyValidator(document, child_node))
        validator[self.key] = child_validator
