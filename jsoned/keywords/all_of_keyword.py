from functools import partial

from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators import ValidatorsMap, ValidatorsCollection
from jsoned.validators.composition_validators import validate_all
from jsoned.validators.deferred_validator import deferred_validator


class AllOfKeyword(AssertionKeyword):
    key = "allOf"

    def apply(self, document: JsonSchema, node: JsonObject, validator: ValidatorsMap):
        if node[self.key].type != JsonType.ARRAY:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.ARRAY)

        all_validator = ValidatorsCollection()

        for child_node in node[self.key]:
            all_validator.append(partial(deferred_validator, schema=document, node=child_node))

        validator[self.key] = partial(validate_all, validators=all_validator)
