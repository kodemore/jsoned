from functools import partial

from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators.array_validators import validate_array_contains
from jsoned.validators.core_validators import ValidatorsMap
from jsoned.validators.deferred_validator import deferred_validator


class ContainsKeyword(AssertionKeyword):
    key = "contains"

    def apply(self, schema: JsonSchema, node: JsonObject, validator: ValidatorsMap):
        if node[self.key].type != JsonType.OBJECT:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.OBJECT)

        if "items" in validator:
            array_validator = validator["items"]
        else:
            array_validator = partial(validate_array_contains, item_validator=partial(deferred_validator, schema=schema, node=node[self.key]))

        if "minContains" in node:
            if node["minContains"].type != JsonType.NUMBER:
                raise SchemaParseError("`minContains` property must be a positive integer.", node.path)
            array_validator = partial(array_validator, minimum_contains = int(node["minContains"].value))

        if "maxContains" in node:
            if node["maxContains"].type != JsonType.NUMBER:
                raise SchemaParseError("`maxContains` property must be a positive integer.", node.path)

            array_validator = partial(array_validator, maximum_contains=int(node["maxContains"].value))

        validator[self.key] = array_validator
