import pytest

from jsoned import JsonSchema
from jsoned.errors import ValidationError, SchemaParseError
from jsoned.keywords import MaximumKeyword
from jsoned.validators import Context


def test_can_instantiate() -> None:
    # given
    keyword = MaximumKeyword()

    # then
    assert isinstance(keyword, MaximumKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "maximum": True,
    }
    keyword = MaximumKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validation() -> None:
    # given
    document = {
        "maximum": 100,
    }
    keyword = MaximumKeyword()
    schema = JsonSchema(document, [keyword])

    # then
    assert schema.validate(0)
    assert schema.validate(1)
    assert schema.validate(20)


def test_can_fail_validation() -> None:
    # given
    document = {
        "maximum": 100,
    }

    keyword = MaximumKeyword()
    schema = JsonSchema(document, [keyword])
    context = Context()
    # when

    assert not schema.validate(101, context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.NUMBER_MAXIMUM_ERROR


def test_can_be_used_with_exclusive_minimum() -> None:
    # given
    document = {
        "maximum": 100,
        "exclusiveMaximum": True,
    }

    keyword = MaximumKeyword()
    schema = JsonSchema(document, [keyword])
    context = Context()

    # then
    assert schema.validate(10)
    assert schema.validate(20)

    # when
    assert not schema.validate(100, context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.NUMBER_EXCLUSIVE_MAXIMUM_ERROR
