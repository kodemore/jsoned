from functools import partial

from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators.core_validators import ValidatorsMap
from jsoned.validators.number_validators import validate_exclusive_maximum


class ExclusiveMaximumKeyword(AssertionKeyword):
    key = "exclusiveMaximum"

    def apply(self, document: JsonSchema, node: JsonObject, validator: ValidatorsMap):
        if node[self.key].type == JsonType.BOOLEAN:
            if "maximum" in node:
                if "maximum" in validator:
                    validator["maximum"] = partial(validator["maximum"], exclusive=True)
                    return

                validator["maximum"] = partial(validate_exclusive_maximum, expected_maximum=node["maximum"].value)

                return
            else:
                raise SchemaParseError.for_keyword_missing_dependency(node, self.key, "maximum")

        if node[self.key].type != JsonType.NUMBER:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.NUMBER)

        validator[self.key] = partial(validate_exclusive_maximum, expected_maximum=node[self.key].value)
