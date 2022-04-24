from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema, LazyValidator
from jsoned.types import JsonObject, JsonType
from jsoned.validators.array_validators import ArrayContainsValidator
from jsoned.validators.core_validators import CompoundValidator


class ContainsKeyword(AssertionKeyword):
    key = "contains"

    def apply(self, schema: JsonSchema, node: JsonObject, validator: CompoundValidator):
        if node[self.key].type != JsonType.OBJECT:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.OBJECT)

        child_validator = ArrayContainsValidator(LazyValidator(schema, node[self.key]))

        if "minContains" in node:
            if node["minContains"].type != JsonType.NUMBER:
                raise SchemaParseError("`minContains` property must be a positive integer.", node.path)
            child_validator.minimum_contains = int(node["minContains"].value)

        if "maxContains" in node:
            if node["maxContains"].type != JsonType.NUMBER:
                raise SchemaParseError("`maxContains` property must be a positive integer.", node.path)
            child_validator.maximum_contains = int(node["maxContains"].value)

        validator[self.key] = child_validator
