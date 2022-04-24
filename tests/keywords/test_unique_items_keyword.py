import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import UniqueItemsKeyword, FormatKeyword, TypeKeyword


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

    # when
    schema.validate(["abc@gmail.com", "ba@test.com"])


def test_can_fail_validation() -> None:
    # given
    document = {
        "uniqueItems": True,
    }
    schema = JsonSchema(document, [UniqueItemsKeyword()])

    # when
    with pytest.raises(ValidationError) as e:
        schema.validate(["abc@gmail.com", "abc@gmail.com"])

    # then
    assert e.value.path == "1"
