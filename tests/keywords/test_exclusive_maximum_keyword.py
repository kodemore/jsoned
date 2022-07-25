import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import ExclusiveMaximumKeyword
from jsoned.validators import Context


def test_can_instantiate() -> None:
    # given
    keyword = ExclusiveMaximumKeyword()

    # then
    assert isinstance(keyword, ExclusiveMaximumKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "exclusiveMaximum": True,
    }
    keyword = ExclusiveMaximumKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validation() -> None:
    # given
    document = {
        "exclusiveMaximum": 10,
    }
    keyword = ExclusiveMaximumKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    assert schema.validate(1)
    assert schema.validate(9)


def test_can_fail_validation() -> None:
    # given
    document = {
        "exclusiveMaximum": 10,
    }

    keyword = ExclusiveMaximumKeyword()
    schema = JsonSchema(document, [keyword])
    context = Context()

    # when
    assert not schema.validate(10, context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.NUMBER_EXCLUSIVE_MAXIMUM_ERROR
