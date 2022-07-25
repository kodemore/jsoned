from functools import partial

from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators.core_validators import ValidatorsMap
from jsoned.validators.number_validators import validate_multiple_of


class MultipleOfKeyword(AssertionKeyword):
    key = "multipleOf"

    def apply(self, document: JsonSchema, node: JsonObject, validator: ValidatorsMap):
        if node[self.key].type != JsonType.NUMBER:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.NUMBER)

        multiple_of = node[self.key].value

        validator[self.key] = partial(validate_multiple_of, multiple_of=multiple_of)
