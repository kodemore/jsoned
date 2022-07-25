from functools import partial

from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators.core_validators import ValidatorsMap
from jsoned.validators.object_validators import validate_object_properties


class UnevaluatedPropertiesKeyword(AssertionKeyword):
    key = "unevaluatedProperties"

    def apply(self, schema: JsonSchema, node: JsonObject, validator: ValidatorsMap):
        if node[self.key].type != JsonType.BOOLEAN:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.BOOLEAN)

        if "object_properties" in validator:
            object_properties = validator["object_properties"]
            object_properties_validator = partial(
                object_properties,
                unevaluated_properties=bool(node[self.key]),
            )
        else:
            object_properties_validator = partial(
                validate_object_properties,
                unevaluated_properties=bool(node[self.key])
            )

        validator["object_properties"] = object_properties_validator

