import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import MaximumLengthKeyword
from jsoned.validators import Context


def test_can_instantiate() -> None:
    # given
    keyword = MaximumLengthKeyword()

    # then
    assert isinstance(keyword, MaximumLengthKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "maxLength": True,
    }
    keyword = MaximumLengthKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validation() -> None:
    # given
    document = {
        "maxLength": 3,
    }
    keyword = MaximumLengthKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    assert schema.validate("abc")


def test_can_fail_validation() -> None:
    # given
    document = {
        "maxLength": 3,
    }

    keyword = MaximumLengthKeyword()
    schema = JsonSchema(document, [keyword])
    context = Context()

    # when
    assert not schema.validate("abcd", context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.STRING_MAXIMUM_LENGTH_ERROR
