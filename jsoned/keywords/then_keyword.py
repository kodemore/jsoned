from functools import partial

from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators import ValidatorsMap
from jsoned.validators.composition_validators import validate_conditionally
from jsoned.validators.deferred_validator import deferred_validator


class ThenKeyword(AssertionKeyword):
    key = "then"

    def apply(self, schema: JsonSchema, node: JsonObject, validator: ValidatorsMap):
        
        if node[self.key].type != JsonType.OBJECT:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.OBJECT)

        # We have to respect if keyword whenever possible
        if "if" in validator:
            child_validator = validator["if"]
            child_validator = partial(
                child_validator,
                condition_then=partial(deferred_validator, schema=schema, node=node[self.key])
            )
        else:
            child_validator = partial(
                validate_conditionally,
                condition_then=partial(deferred_validator, schema=schema, node=node[self.key])
            )

        validator["if"] = child_validator
