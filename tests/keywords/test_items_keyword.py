import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import ItemsKeyword, FormatKeyword, TypeKeyword
from jsoned.validators import Context


def test_can_instantiate() -> None:
    # given
    keyword = ItemsKeyword()

    # then
    assert isinstance(keyword, ItemsKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "items": 12,
    }
    keyword = ItemsKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate([])


def test_can_pass_validation() -> None:
    # given
    document = {
       "items": {
           "format": "email",
       }
    }
    schema = JsonSchema(document, [ItemsKeyword(), FormatKeyword()])

    # when
    assert schema.validate(["abc@gmail.com", "ba@test.com"])


def test_can_fail_validation() -> None:
    # given
    document = {
        "items": {
            "format": "email",
        }
    }
    schema = JsonSchema(document, [ItemsKeyword(), FormatKeyword()])
    context = Context()

    # when
    assert not schema.validate(["abc@gmail.com", "test"], context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.STRING_FORMAT_ERROR
    assert context.errors[0].path == "1"


def test_can_validate_legacy_tuple_format() -> None:
    # given
    document = {
        "items": [
            {"format": "email"},
            {"type": "number"},
            {"type": "boolean"},
        ]
    }
    schema = JsonSchema(document, [ItemsKeyword(), TypeKeyword(), FormatKeyword()])
    context = Context()

    # tuple may contain exact amount of items
    assert schema.validate(["abc@gmail.com", 12.4, True])

    # tuple may contain more items if not specified otherwise
    assert schema.validate(["abc@gmail.com", 12.4, True, "extra"])

    # tuple may contain less items than specified
    assert schema.validate(["abc@gmail.com", 12.3])

    # tuple fails when items are invalid
    assert not schema.validate([12.3], context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.STRING_FORMAT_ERROR
    assert context.errors[0].path == "0"
