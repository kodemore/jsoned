from functools import partial

from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators.core_validators import fail_validation, ValidatorsMap
from jsoned.validators.deferred_validator import deferred_validator
from jsoned.validators.object_validators import validate_object_properties


class AdditionalPropertiesKeyword(AssertionKeyword):
    key = "additionalProperties"

    def apply(self, document: JsonSchema, node: JsonObject, validator: ValidatorsMap):
        if node[self.key].type != JsonType.OBJECT and node[self.key].type != JsonType.BOOLEAN:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.OBJECT)

        if node[self.key].type == JsonType.BOOLEAN and node[self.key]:
            return  # additional properties are allowed

        if "object_properties" in validator:
            validate_object = validator["object_properties"]
        else:
            validate_object = validate_object_properties

        # no additional properties should be present
        if node[self.key].type == JsonType.BOOLEAN:
            validator["object_properties"] = partial(validate_object, additional_properties=fail_validation)
            return

        # nested validator for additional properties
        validator["object_properties"] = partial(
            validate_object,
            additional_properties=partial(deferred_validator, schema=document, node=node[self.key])
        )
