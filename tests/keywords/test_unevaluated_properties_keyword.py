import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import PropertiesKeyword, UnevaluatedPropertiesKeyword, TypeKeyword, FormatKeyword
from jsoned.validators import Context


def test_can_instantiate() -> None:
    # given
    keyword = UnevaluatedPropertiesKeyword()

    # then
    assert isinstance(keyword, UnevaluatedPropertiesKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "unevaluatedProperties": "abc",
    }
    keyword = UnevaluatedPropertiesKeyword()
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
        "unevaluatedProperties": False,
    }
    keywords = [UnevaluatedPropertiesKeyword(), PropertiesKeyword(), TypeKeyword(), FormatKeyword()]
    schema = JsonSchema(document, keywords)

    # when
    assert schema.validate({
        "name": "Bob",
    })


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
        "unevaluatedProperties": False
    }
    keywords = [PropertiesKeyword(), UnevaluatedPropertiesKeyword(), TypeKeyword(), FormatKeyword()]
    schema = JsonSchema(document, keywords)
    context = Context()

    # when
    assert not schema.validate({"extra": 1}, context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.PROPERTY_UNEVALUATED_ERROR
