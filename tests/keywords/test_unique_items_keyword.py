import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import UniqueItemsKeyword
from jsoned.validators import Context


def test_can_instantiate() -> None:
    # given
    keyword = UniqueItemsKeyword()

    # then
    assert isinstance(keyword, UniqueItemsKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "uniqueItems": 12,
    }
    keyword = UniqueItemsKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate([])


def test_can_pass_validation() -> None:
    # given
    document = {
       "uniqueItems": True,
    }
    schema = JsonSchema(document, [UniqueItemsKeyword()])

    # then
    assert schema.validate(["abc@gmail.com", "ba@test.com"])


def test_can_fail_validation() -> None:
    # given
    document = {
        "uniqueItems": True,
    }
    schema = JsonSchema(document, [UniqueItemsKeyword()])
    context = Context()

    # when
    assert not schema.validate(["abc@gmail.com", "abc@gmail.com"], context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.ARRAY_NON_UNIQUE_ERROR
    assert context.errors[0].path == "1"
