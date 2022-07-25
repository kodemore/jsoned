from functools import partial

from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators.core_validators import ValidatorsMap
from jsoned.validators.deferred_validator import deferred_validator
from jsoned.validators.object_validators import validate_object_properties


class PropertiesKeyword(AssertionKeyword):
    key = "properties"

    def apply(self, schema: JsonSchema, node: JsonObject, validator: ValidatorsMap):
        if node[self.key].type != JsonType.OBJECT:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.OBJECT)

        properties_validators = ValidatorsMap[str]()

        for key, value in node[self.key].items():
            properties_validators[key] = partial(
                deferred_validator,
                schema=schema,
                node=value,
            )

        if "object_properties" in validator:
            object_properties = validator["object_properties"]
            object_properties = partial(
                object_properties,
                properties=properties_validators,
            )
        else:
            object_properties = partial(
                validate_object_properties,
                properties=properties_validators,
            )

        validator["object_properties"] = object_properties
