import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import MinimumItemsKeyword
from jsoned.validators import Context


def test_can_instantiate() -> None:
    # given
    keyword = MinimumItemsKeyword()

    # then
    assert isinstance(keyword, MinimumItemsKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "minItems": True,
    }
    keyword = MinimumItemsKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validation() -> None:
    # given
    document = {
        "minItems": 3,
    }
    keyword = MinimumItemsKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    assert schema.validate([1, 2, 3])


def test_can_fail_validation() -> None:
    # given
    document = {
        "minItems": 3,
    }

    keyword = MinimumItemsKeyword()
    schema = JsonSchema(document, [keyword])
    context = Context()

    # when
    assert not schema.validate([1], context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.ARRAY_MIN_LENGTH_ERROR
