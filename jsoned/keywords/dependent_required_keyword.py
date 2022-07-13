from functools import partial

from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators import ValidatorsMap
from jsoned.validators.object_validators import validate_dependent_required_properties


class DependentRequiredKeyword(AssertionKeyword):
    key = "dependentRequired"

    def apply(self, document: JsonSchema, node: JsonObject, validator: ValidatorsMap):
        if node[self.key].type != JsonType.OBJECT:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.OBJECT)

        dependency_map = {key: [str(item) for item in items] for key, items in node[self.key].items()}

        child_validator = partial(validate_dependent_required_properties, dependency_map=dependency_map)
        validator[self.key] = child_validator
