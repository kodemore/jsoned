from functools import partial

from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators import ValidatorsMap
from jsoned.validators.composition_validators import validate_not
from jsoned.validators.deferred_validator import deferred_validator


class NotKeyword(AssertionKeyword):
    key = "not"

    def apply(self, schema: JsonSchema, node: JsonObject, validator: ValidatorsMap):
        if node[self.key].type != JsonType.OBJECT and node[self.key].type != JsonType.BOOLEAN:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.OBJECT)

        child_validator = partial(
            validate_not,
            validator=partial(
                deferred_validator,
                schema=schema,
                node=node[self.key]
            )
        )

        validator[self.key] = child_validator
