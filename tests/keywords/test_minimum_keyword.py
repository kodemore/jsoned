import pytest

from jsoned import JsonSchema
from jsoned.errors import ValidationError, SchemaParseError
from jsoned.keywords import MinimumKeyword
from jsoned.validators import Context


def test_can_instantiate() -> None:
    # given
    keyword = MinimumKeyword()

    # then
    assert isinstance(keyword, MinimumKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "minimum": True,
    }
    keyword = MinimumKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validation() -> None:
    # given
    document = {
        "minimum": 0,
    }
    keyword = MinimumKeyword()
    schema = JsonSchema(document, [keyword])

    # then
    assert schema.validate(0)
    assert schema.validate(1)
    assert schema.validate(20)


def test_can_fail_validation() -> None:
    # given
    document = {
        "minimum": 0,
    }

    keyword = MinimumKeyword()
    schema = JsonSchema(document, [keyword])
    context = Context()

    # when
    assert not schema.validate(-1, context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.NUMBER_MINIMUM_ERROR


def test_can_be_used_with_exclusive_minimum() -> None:
    # given
    document = {
        "minimum": 0,
        "exclusiveMinimum": True,
    }

    keyword = MinimumKeyword()
    schema = JsonSchema(document, [keyword])
    context = Context()

    # then
    assert schema.validate(1)
    assert schema.validate(2)

    # when
    assert not schema.validate(0, context)

    # then
    assert len(context.errors) == 1
