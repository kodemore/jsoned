import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import PropertiesKeyword, UnevaluatedPropertiesKeyword, TypeKeyword, FormatKeyword


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
    schema.validate({
        "name": "Bob",
    })

    # then
    assert "properties" in schema.validator
    assert schema.validator["properties"].unevaluated_properties


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

    # when
    with pytest.raises(ValidationError) as e:
        schema.validate({"extra": 1})

    assert e.value.path == "extra"
