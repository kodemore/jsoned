from functools import partial

from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators.array_validators import validate_array_items, validate_array_prefixed_items
from jsoned.validators.core_validators import ValidatorsMap, ValidatorsCollection, fail_validation
from jsoned.validators.deferred_validator import deferred_validator


class ItemsKeyword(AssertionKeyword):
    key = "items"

    def apply(self, schema: JsonSchema, node: JsonObject, validator: ValidatorsMap):
        if node[self.key].type in [JsonType.STRING, JsonType.NULL, JsonType.NUMBER]:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.OBJECT)

        # items with prefixed items should be handled by PrefixedItemsKeyword
        if "prefixItems" in node:
            return

        # array prefixed items validator
        if node[self.key].type == JsonType.ARRAY:
            items_validator = ValidatorsCollection()
            for item in node[self.key]:
                items_validator.append(partial(deferred_validator, schema=schema, node=item))

            child_validator = partial(validate_array_prefixed_items, items_validator=items_validator)

            # extra items can be allowed or contain its own validator
            if "additionalItems" in node:
                if node["additionalItems"].type == JsonType.BOOLEAN:
                    child_validator = partial(child_validator, additional_items=node["additionalItems"].value)
                elif node["additionalItems"].type == JsonType.OBJECT:
                    child_validator = partial(
                        child_validator,
                        additional_items=partial(deferred_validator, schema=schema, node=node["additionalItems"])
                    )
                else:
                    raise SchemaParseError.for_invalid_keyword_value(node, "additionalItems", JsonType.OBJECT)

        # array validator
        elif node[self.key].type == JsonType.OBJECT:
            child_validator = partial(
                validate_array_items,
                items_validator=partial(deferred_validator, schema=schema, node=node[self.key])
            )

        elif node[self.key].type == JsonType.BOOLEAN and not node[self.key]:
            child_validator = partial(
                validate_array_items,
                items_validator=fail_validation
            )
        else:
            # items can be of boolean type and support indexedItems keyword and we ignore this
            # option here

            return

        validator[self.key] = child_validator
