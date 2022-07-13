import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import PrefixItemsKeyword, FormatKeyword
from jsoned.validators import Context


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

    # then
    assert schema.validate(["abc@gmail.com"])


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
    context = Context()

    # when
    assert not schema.validate([".com"], context)

    # then
    assert context.errors[0].code == ValidationError.ErrorCodes.STRING_FORMAT_ERROR
    assert context.errors[0].path == "0"
