from functools import partial

from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators.array_validators import validate_array_prefixed_items
from jsoned.validators.core_validators import ValidatorsMap, ValidatorsCollection
from jsoned.validators.deferred_validator import deferred_validator


class PrefixItemsKeyword(AssertionKeyword):
    key = "prefixItems"

    def apply(self, schema: JsonSchema, node: JsonObject, validator: ValidatorsMap):
        if node[self.key].type != JsonType.ARRAY:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.ARRAY)

        items_validator = ValidatorsCollection()
        for child_node in node[self.key]:
            items_validator.append(partial(
                deferred_validator,
                schema=schema,
                node=child_node,
            ))

        if "items" in node and node["items"].type == JsonType.OBJECT:
            additional_items = partial(
                deferred_validator,
                schema=schema,
                node=node["items"]
            )
        elif "items" in node and node["items"].type == JsonType.BOOLEAN:
            additional_items = bool(node["items"])
        else:
            additional_items = False

        validator[self.key] = partial(
            validate_array_prefixed_items,
            items_validator=items_validator,
            additional_items=additional_items
        )
