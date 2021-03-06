from jsoned.errors import SchemaParseError
from jsoned.json_core import AssertionKeyword, JsonSchema
from jsoned.string_format import StringFormat
from jsoned.types import JsonObject, JsonType
from jsoned.validators.core_validators import CompoundValidator
from jsoned.validators.string_validators import StringFormatValidator


class FormatKeyword(AssertionKeyword):
    key = "format"

    def apply(self, document: JsonSchema, node: JsonObject, validator: CompoundValidator):
        if node[self.key].type != JsonType.STRING:
            raise SchemaParseError.for_invalid_keyword_value(node, self.key, JsonType.STRING)

        format_name = str(node[self.key])
        if format_name not in StringFormat:
            raise SchemaParseError(
                f"Parsing failed at `{node.path}`. Unrecognized format type `{format_name}`."
                f"Please use {StringFormat.__class__.__name__} to register your custom format type.",
                node.path
            )

        validator[self.key] = StringFormatValidator(expected_format=format_name)
