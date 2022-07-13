import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import OneOfKeyword, TypeKeyword
from jsoned.validators import Context


def test_can_instantiate() -> None:
    # given
    keyword = OneOfKeyword()

    # then
    assert isinstance(keyword, OneOfKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "oneOf": 12,
    }
    keyword = OneOfKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validate() -> None:
    # given
    document = {
        "oneOf": [
            {"type": "string"},
            {"type": "integer"},
        ],
    }
    schema = JsonSchema(document, [OneOfKeyword(), TypeKeyword()])

    # then
    assert schema.validate("test")
    assert schema.validate(12)


def test_can_fail_validation() -> None:
    # given
    document = {
        "oneOf": [
            {"type": "string"},
            {"type": "integer"},
            {"type": "string"},
        ],
    }
    schema = JsonSchema(document, [OneOfKeyword(), TypeKeyword()])
    context = Context()

    # when
    assert not schema.validate("a", context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.ONE_OF_ERROR

    # when
    context = Context()
    assert not schema.validate(False, context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.ONE_OF_ERROR

