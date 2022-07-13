from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators import ValidatorsMap
from jsoned.validators.object_validators import validate_dependent_schemas
from jsoned.validators.deferred_validator import deferred_validator
from functools import partial


class DependentSchemasKeyword(AssertionKeyword):
    key = "dependentSchemas"

    def apply(self, document: JsonSchema, node: JsonObject, validator: ValidatorsMap):
        if node[self.key].type != JsonType.OBJECT:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.OBJECT)

        dependent_schemas = ValidatorsMap()
        for key, child_node in node[self.key].items():
            dependent_schemas[key] = partial(deferred_validator, schema=document, node=child_node)

        validator[self.key] = partial(validate_dependent_schemas, dependent_schemas=dependent_schemas)
