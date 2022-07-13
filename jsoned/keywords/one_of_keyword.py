from functools import partial

from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators.composition_validators import validate_one_of
from jsoned.validators.core_validators import ValidatorsMap, ValidatorsCollection
from jsoned.validators.deferred_validator import deferred_validator


class OneOfKeyword(AssertionKeyword):
    key = "oneOf"

    def apply(self, schema: JsonSchema, node: JsonObject, validator: ValidatorsMap):
        if node[self.key].type != JsonType.ARRAY:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.ARRAY)

        one_of_validators = ValidatorsCollection()
        for child_node in node[self.key]:
            one_of_validators.append(partial(
                deferred_validator,
                schema=schema,
                node=child_node
            ))

        validator[self.key] = partial(validate_one_of, validators=one_of_validators)
