from functools import partial

from jsoned.errors.schema_parse_error import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.types import JsonObject, JsonType
from jsoned.validators import ValidatorsMap
from jsoned.validators.object_validators import validate_dependent_required_properties


class DependentRequiredKeyword(AssertionKeyword):
    key = ["dependentRequired", "dependencies"]

    def apply(self, document: JsonSchema, node: JsonObject, validator: ValidatorsMap):
        keyword = "dependentRequired" if "dependentRequired" in node else "dependencies"

        if node[keyword].type != JsonType.OBJECT:
            raise SchemaParseError.for_invalid_keyword_value(node, keyword, JsonType.OBJECT)

        dependency_map = {key: [str(item) for item in items] for key, items in node[keyword].items()}

        child_validator = partial(validate_dependent_required_properties, dependency_map=dependency_map)
        validator["dependentRequired"] = child_validator
