from functools import partial

from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators.array_validators import validate_array_unevaluated_items
from jsoned.validators.core_validators import ValidatorsMap
from jsoned.validators.deferred_validator import deferred_validator


class UnevaluatedItemsKeyword(AssertionKeyword):
    key = "unevaluatedItems"

    def apply(self, schema: JsonSchema, node: JsonObject, validator: ValidatorsMap):
        if node[self.key].type not in [JsonType.BOOLEAN, JsonType.OBJECT]:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.BOOLEAN)

        if "prefixItems" in node and "items" in node:
            return  # this is negating additional items

        # items validator
        if node[self.key].type == JsonType.OBJECT:
            child_validator = partial(
                validate_array_unevaluated_items,
                item_validator=partial(deferred_validator, schema=schema, node=node[self.key])
            )
        elif node[self.key].type == JsonType.BOOLEAN and node[self.key]:
            return  # allow unevaluated items
        else:
            child_validator = validate_array_unevaluated_items

        validator[self.key] = child_validator
