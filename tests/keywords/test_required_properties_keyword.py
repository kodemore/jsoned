import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import RequiredPropertiesKeyword, TypeKeyword, FormatKeyword, PropertiesKeyword


def test_can_instantiate() -> None:
    # given
    keyword = RequiredPropertiesKeyword()

    # then
    assert isinstance(keyword, RequiredPropertiesKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "required": 123,
    }
    keyword = RequiredPropertiesKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validate() -> None:
    # given
    document = {
        "required": ["a", "b"]
    }
    keywords = [RequiredPropertiesKeyword(), TypeKeyword(), FormatKeyword()]
    schema = JsonSchema(document, keywords)

    # when
    schema.validate({
        "a": 1,
        "b": 2,
        "c": 3,
    })

    # then
    assert "required" in schema.validator


def test_can_fail_validation() -> None:
    # given
    document = {
        "required": ["a", "b"]
    }
    keywords = [RequiredPropertiesKeyword(), TypeKeyword(), FormatKeyword()]
    schema = JsonSchema(document, keywords)

    # when
    with pytest.raises(ValidationError) as e:
        schema.validate({
            "a": 123,
        })

    # then
    error = e.value
    assert error.path == ""
