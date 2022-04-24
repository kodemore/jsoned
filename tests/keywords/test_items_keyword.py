import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import ItemsKeyword, FormatKeyword, TypeKeyword


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
    schema.validate(["abc@gmail.com", "ba@test.com"])


def test_can_fail_validation() -> None:
    # given
    document = {
        "items": {
            "format": "email",
        }
    }
    schema = JsonSchema(document, [ItemsKeyword(), FormatKeyword()])

    # when
    with pytest.raises(ValidationError) as e:
        schema.validate(["abc@gmail.com", "test"])

    # then
    assert e.value.path == "1"


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

    # then
    schema.validate(["abc@gmail.com", 12.4, True])

    # when
    with pytest.raises(ValidationError) as e:
        schema.validate(["abc@gmail.com", 12.3])

    assert e.value.path == "2"
