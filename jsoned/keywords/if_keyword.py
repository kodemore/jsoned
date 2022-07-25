from functools import partial

from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators import ValidatorsMap
from jsoned.validators.composition_validators import validate_conditionally
from jsoned.validators.deferred_validator import deferred_validator


class IfKeyword(AssertionKeyword):
    key = "if"

    def apply(self, document: JsonSchema, node: JsonObject, validator: ValidatorsMap):
        if node[self.key].type != JsonType.OBJECT and node[self.key].type != JsonType.BOOLEAN:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.OBJECT)

        # if then and else is not present if should be ignored
        if "then" not in node and "else" not in node:
            return

        child_validator = validate_conditionally

        # This may happen if else keyword was registered before if keyword
        if self.key in validator:
            child_validator = validator[self.key]

        child_validator = partial(
            child_validator,
            condition_if=partial(deferred_validator, schema=document, node=node[self.key])
        )

        validator[self.key] = child_validator
