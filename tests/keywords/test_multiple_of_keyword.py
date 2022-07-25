import pytest

from jsoned import JsonSchema
from jsoned.errors import ValidationError, SchemaParseError
from jsoned.keywords import MultipleOfKeyword
from jsoned.validators import Context


def test_can_instantiate() -> None:
    # given
    keyword = MultipleOfKeyword()

    # then
    assert isinstance(keyword, MultipleOfKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "multipleOf": True,
    }
    keyword = MultipleOfKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validation() -> None:
    # given
    document = {
        "multipleOf": 10,
    }
    keyword = MultipleOfKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    assert schema.validate(0)
    assert schema.validate(10)
    assert schema.validate(20)


def test_can_fail_validation() -> None:
    # given
    document = {
        "multipleOf": 10,
    }

    keyword = MultipleOfKeyword()
    schema = JsonSchema(document, [keyword])
    context = Context()

    # when
    assert not schema.validate(23, context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.NUMBER_MULTIPLE_OF_ERROR
