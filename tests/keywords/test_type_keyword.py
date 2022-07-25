import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import TypeKeyword
from jsoned.validators import Context


def test_can_instantiate() -> None:
    # given
    keyword = TypeKeyword()

    # then
    assert isinstance(keyword, TypeKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "type": "unknown",
    }
    keyword = TypeKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validate() -> None:
    # given
    document = {
        "type": "boolean"
    }
    keyword = TypeKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    assert schema.validate(True)


def test_can_fail_validation() -> None:
    # given
    document = {
        "type": "boolean"
    }
    keyword = TypeKeyword()
    schema = JsonSchema(document, [keyword])
    context = Context()

    # when
    assert not schema.validate("1", context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.TYPE_ERROR
