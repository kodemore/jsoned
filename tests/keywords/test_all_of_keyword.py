import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import AllOfKeyword, TypeKeyword, MaximumLengthKeyword


def test_can_instantiate() -> None:
    # given
    keyword = AllOfKeyword()

    # then
    assert isinstance(keyword, AllOfKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "allOf": 12,
    }
    keyword = AllOfKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validate() -> None:
    # given
    document = {
        "allOf": [
            {"type": "string"},
            {"maxLength": 10},
        ],
    }
    schema = JsonSchema(document, [AllOfKeyword(), TypeKeyword(), MaximumLengthKeyword()])

    # when
    schema.validate("test")


def test_can_fail_validation() -> None:
    # given
    document = {
        "allOf": [
            {"type": "string"},
            {"maxLength": 10},
        ],
    }
    schema = JsonSchema(document, [AllOfKeyword(), TypeKeyword(), MaximumLengthKeyword()])

    # when
    with pytest.raises(ValidationError) as e:
        schema.validate("too long to pass the test")

    # then
    assert e.value.path == ""

    with pytest.raises(ValidationError) as e:
        schema.validate(11)

    # then
    assert e.value.path == ""

