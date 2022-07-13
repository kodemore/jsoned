import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError
from jsoned.errors import ValidationError
from jsoned.keywords import MinimumLengthKeyword
from jsoned.validators import Context


def test_can_instantiate() -> None:
    # given
    keyword = MinimumLengthKeyword()

    # then
    assert isinstance(keyword, MinimumLengthKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "minLength": True,
    }
    keyword = MinimumLengthKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validation() -> None:
    # given
    document = {
        "minLength": 3,
    }
    keyword = MinimumLengthKeyword()
    schema = JsonSchema(document, [keyword])

    # then
    assert schema.validate("abc")


def test_can_fail_validation() -> None:
    # given
    document = {
        "minLength": 3,
    }

    keyword = MinimumLengthKeyword()
    schema = JsonSchema(document, [keyword])
    context = Context()

    # when
    assert not schema.validate("1", context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.STRING_MINIMUM_LENGTH_ERROR
