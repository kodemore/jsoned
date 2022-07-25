from functools import partial

from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators.core_validators import ValidatorsMap
from jsoned.validators.deferred_validator import deferred_validator
from jsoned.validators.object_validators import validate_object_properties


class PropertyNamesKeyword(AssertionKeyword):
    key = "propertyNames"

    def apply(self, schema: JsonSchema, node: JsonObject, validator: ValidatorsMap):
        if node[self.key].type != JsonType.OBJECT and node[self.key].type != JsonType.BOOLEAN:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.OBJECT)

        if "object_properties" in validator:
            object_properties = validator["object_properties"]
            object_properties = partial(
                object_properties,
                property_names=partial(
                    deferred_validator,
                    schema=schema,
                    node=node[self.key],
                ),
            )
        else:
            object_properties = partial(
                validate_object_properties,
                property_names=partial(
                    deferred_validator,
                    schema=schema,
                    node=node[self.key],
                ),
            )

        validator["object_properties"] = object_properties
