from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema, LazyValidator
from jsoned.types import JsonObject, JsonType
from jsoned.validators import CompoundValidator
from jsoned.validators.object_validators import DependentSchemasValidator


class DependentSchemasKeyword(AssertionKeyword):
    key = "dependentSchemas"

    def apply(self, document: JsonSchema, node: JsonObject, validator: CompoundValidator):
        if node[self.key].type != JsonType.OBJECT:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.OBJECT)

        child_validator = DependentSchemasValidator()
        for key, child_node in node[self.key].items():
            child_validator[key] = LazyValidator(document, child_node)

        validator[self.key] = child_validator
