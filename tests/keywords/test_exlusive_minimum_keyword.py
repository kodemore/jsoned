import pytest

from jsoned import JsonSchema
from jsoned.errors import ValidationError, SchemaParseError
from jsoned.keywords import ExclusiveMinimumKeyword
from jsoned.validators import Context


def test_can_instantiate() -> None:
    # given
    keyword = ExclusiveMinimumKeyword()

    # then
    assert isinstance(keyword, ExclusiveMinimumKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "exclusiveMinimum": True,
    }
    keyword = ExclusiveMinimumKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validation() -> None:
    # given
    document = {
        "exclusiveMinimum": 0,
    }
    keyword = ExclusiveMinimumKeyword()
    schema = JsonSchema(document, [keyword])

    # then
    assert schema.validate(1)
    assert schema.validate(20)


def test_can_fail_validation() -> None:
    # given
    document = {
        "exclusiveMinimum": 0,
    }

    keyword = ExclusiveMinimumKeyword()
    schema = JsonSchema(document, [keyword])
    context = Context()

    # when
    assert not schema.validate(0, context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.NUMBER_EXCLUSIVE_MINIMUM_ERROR
