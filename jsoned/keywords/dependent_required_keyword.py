from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators import CompoundValidator
from jsoned.validators.object_validators import DependentRequiredValidator


class DependentRequiredKeyword(AssertionKeyword):
    key = "dependentRequired"

    def apply(self, document: JsonSchema, node: JsonObject, validator: CompoundValidator):
        if node[self.key].type != JsonType.OBJECT:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.OBJECT)

        child_validator = DependentRequiredValidator({key: [str(item) for item in items] for key, items in node[self.key].items()})
        validator[self.key] = child_validator
