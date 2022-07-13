import pytest

from jsoned import JsonSchema
from jsoned.errors import ValidationError
from jsoned.errors import SchemaParseError
from jsoned.keywords import MaximumItemsKeyword
from jsoned.validators import Context


def test_can_instantiate() -> None:
    # given
    keyword = MaximumItemsKeyword()

    # then
    assert isinstance(keyword, MaximumItemsKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "maxItems": True,
    }
    keyword = MaximumItemsKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validation() -> None:
    # given
    document = {
        "maxItems": 3,
    }
    keyword = MaximumItemsKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    assert schema.validate([1, 2, 3])


def test_can_fail_validation() -> None:
    # given
    document = {
        "maxItems": 3,
    }

    keyword = MaximumItemsKeyword()
    schema = JsonSchema(document, [keyword])
    context = Context()

    # when

    assert not schema.validate([1, 2, 3, 5], context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.ARRAY_MAX_LENGTH_ERROR
