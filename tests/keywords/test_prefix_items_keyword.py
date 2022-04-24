import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import PrefixItemsKeyword, FormatKeyword, TypeKeyword


def test_can_instantiate() -> None:
    # given
    keyword = PrefixItemsKeyword()

    # then
    assert isinstance(keyword, PrefixItemsKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "prefixItems": 12,
    }
    keyword = PrefixItemsKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate([])


def test_can_pass_validation() -> None:
    # given
    document = {
        "prefixItems": [
            {
                "format": "email",
            },
        ]
    }
    schema = JsonSchema(document, [PrefixItemsKeyword(), FormatKeyword()])

    # when
    schema.validate(["abc@gmail.com"])


def test_can_fail_validation() -> None:
    # given
    document = {
        "prefixItems": [
            {
                "format": "email",
            },
        ]
    }
    schema = JsonSchema(document, [PrefixItemsKeyword(), FormatKeyword()])

    # when
    with pytest.raises(ValidationError) as e:
        schema.validate([".com"])

    # then
    assert e.value.path == "0"
