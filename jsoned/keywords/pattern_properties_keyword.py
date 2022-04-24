from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema, LazyValidator
from jsoned.types import JsonObject, JsonType
from jsoned.validators.object_validators import PropertiesValidator
from jsoned.validators.core_validators import CompoundValidator


class PatternPropertiesKeyword(AssertionKeyword):
    key = "patternProperties"

    def apply(self, document: JsonSchema, node: JsonObject, validator: CompoundValidator):
        if node[self.key].type != JsonType.OBJECT:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.OBJECT)

        if "properties" not in validator:
            validator["properties"] = PropertiesValidator()

        validator["properties"].pattern_properties = CompoundValidator()

        for key, value in node[self.key].items():
            validator["properties"].pattern_properties[key] = LazyValidator(document, value)
