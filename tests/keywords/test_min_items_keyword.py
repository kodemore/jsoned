import pytest

from jsoned import JsonSchema
from jsoned.errors import MinimumItemsValidationError
from jsoned.errors import SchemaParseError
from jsoned.keywords import MinimumItemsKeyword


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
    schema.validate([1, 2, 3])


def test_can_fail_validation() -> None:
    # given
    document = {
        "minItems": 3,
    }

    keyword = MinimumItemsKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(MinimumItemsValidationError) as e:
        schema.validate([1])

    # then
    assert e.value.expected_minimum == 3
