import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import PropertiesKeyword, AdditionalPropertiesKeyword, TypeKeyword, FormatKeyword
from jsoned.validators import Context


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
    valid = schema.validate({
        "name": "Bob",
        "age": 11
    })

    # then
    assert valid


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
    assert schema.validate({"email": "test@email.com"})

    context = Context()
    assert not schema.validate({"extra": 1}, context)

    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.PROPERTY_UNEXPECTED_ADDITIONAL_PROPERTY_ERROR
