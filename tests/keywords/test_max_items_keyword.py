import pytest

from jsoned import JsonSchema
from jsoned.errors import MaximumItemsValidationError
from jsoned.errors import SchemaParseError
from jsoned.keywords import MaximumItemsKeyword


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
    schema.validate([1, 2, 3])


def test_can_fail_validation() -> None:
    # given
    document = {
        "maxItems": 3,
    }

    keyword = MaximumItemsKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(MaximumItemsValidationError) as e:
        schema.validate([1, 2, 3, 5])

    # then
    assert e.value.expected_maximum == 3
