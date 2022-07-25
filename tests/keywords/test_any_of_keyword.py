import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import AnyOfKeyword, TypeKeyword
from jsoned.validators import Context


def test_can_instantiate() -> None:
    # given
    keyword = AnyOfKeyword()

    # then
    assert isinstance(keyword, AnyOfKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "anyOf": 12,
    }
    keyword = AnyOfKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validate() -> None:
    # given
    document = {
        "anyOf": [
            {"type": "string"},
            {"type": "integer"},
        ],
    }
    schema = JsonSchema(document, [AnyOfKeyword(), TypeKeyword()])

    # then
    assert schema.validate("test")
    assert schema.validate(12)


def test_can_fail_validation() -> None:
    # given
    document = {
        "anyOf": [
            {"type": "string"},
            {"type": "integer"},
        ],
    }
    schema = JsonSchema(document, [AnyOfKeyword(), TypeKeyword()])
    context = Context()

    # when
    assert not schema.validate(11.2, context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.ANY_OF_ERROR

    # when
    context = Context()
    assert not schema.validate(False, context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.ANY_OF_ERROR
