import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.json_core import LazyValidator
from jsoned.keywords import PropertiesKeyword, AdditionalPropertiesKeyword, TypeKeyword, FormatKeyword


def test_can_instantiate() -> None:
    # given
    keyword = AdditionalPropertiesKeyword()

    # then
    assert isinstance(keyword, AdditionalPropertiesKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "additionalProperties": "abc",
    }
    keyword = AdditionalPropertiesKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate({"a": 1})


def test_can_pass_validate() -> None:
    # given
    document = {
        "properties": {
            "name": {
                "type": "string",
            },
            "email": {
                "type": "string",
                "format": "email",
            }
        },
        "additionalProperties": {
            "type": "integer",
        }
    }
    keywords = [AdditionalPropertiesKeyword(), PropertiesKeyword(), TypeKeyword(), FormatKeyword()]
    schema = JsonSchema(document, keywords)

    # when
    schema.validate({
        "name": "Bob",
        "age": 11
    })

    # then
    assert "properties" in schema.validator
    assert isinstance(schema.validator["properties"].additional_properties, LazyValidator)


def test_can_fail_validation() -> None:
    # given
    document = {
        "properties": {
            "name": {
                "type": "string",
            },
            "email": {
                "type": "string",
                "format": "email",
            }
        },
        "additionalProperties": False
    }
    keywords = [PropertiesKeyword(), AdditionalPropertiesKeyword(), TypeKeyword(), FormatKeyword()]
    schema = JsonSchema(document, keywords)

    # when
    schema.validate({"email": "test@email.com"})

    with pytest.raises(ValidationError) as e:
        schema.validate({"extra": 1})
