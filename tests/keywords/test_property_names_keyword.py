import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import PropertyNamesKeyword, TypeKeyword, PatternKeyword


def test_can_instantiate() -> None:
    # given
    keyword = PropertyNamesKeyword()

    # then
    assert isinstance(keyword, PropertyNamesKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "propertyNames": "abc",
    }
    keyword = PropertyNamesKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validate() -> None:
    # given
    document = {
        "propertyNames": {
            "pattern": "^an?_"
        }
    }
    keywords = [PropertyNamesKeyword(), PatternKeyword()]
    schema = JsonSchema(document, keywords)

    # when
    schema.validate({
        "a_name": "Bob",
        "an_email": "bob@builder.com",
    })

    # then
    assert "properties" in schema.validator
    assert schema.validator["properties"].property_names


def test_can_fail_validation() -> None:
    # given
    document = {
        "propertyNames": {
            "pattern": "^an?_"
        }
    }
    keywords = [PropertyNamesKeyword(), PatternKeyword()]
    schema = JsonSchema(document, keywords)

    # when
    with pytest.raises(ValidationError) as e:
        schema.validate({"email": "invalid"})

    assert e.value.path == "email"
