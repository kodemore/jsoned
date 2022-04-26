from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema, LazyValidator
from jsoned.types import JsonObject, JsonType
from jsoned.validators import CompoundValidator
from jsoned.validators.composition_validators import NotValidator


class NotKeyword(AssertionKeyword):
    key = "not"

    def apply(self, document: JsonSchema, node: JsonObject, validator: CompoundValidator):
        if node[self.key].type != JsonType.OBJECT:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.OBJECT)

        child_validator = NotValidator(LazyValidator(document, node[self.key]))
        validator[self.key] = child_validator
