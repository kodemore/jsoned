from functools import partial

from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators.core_validators import ValidatorsMap
from jsoned.validators.number_validators import validate_exclusive_minimum


class ExclusiveMinimumKeyword(AssertionKeyword):
    key = "exclusiveMinimum"

    def apply(self, document: JsonSchema, node: JsonObject, validator: ValidatorsMap):
        if node[self.key].type == JsonType.BOOLEAN:
            if "minimum" in node:
                if "minimum" in validator:
                    validator["minimum"] = partial(validator["minimum"], exclusive=True)
                    return

                validator["minimum"] = partial(validate_exclusive_minimum, expected_minimum=node["minimum"].value)

                return
            else:
                raise SchemaParseError.for_keyword_missing_dependency(node, self.key, "minimum")

        if node[self.key].type != JsonType.NUMBER:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.NUMBER)

        validator[self.key] = partial(validate_exclusive_minimum, expected_minimum=node[self.key].value)
