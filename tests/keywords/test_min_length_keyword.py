import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError
from jsoned.errors.string_validation_errors import MinimumLengthValidationError, LengthValidationError
from jsoned.keywords import MinimumLengthKeyword


def test_can_instantiate() -> None:
    # given
    keyword = MinimumLengthKeyword()

    # then
    assert isinstance(keyword, MinimumLengthKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "minLength": True,
    }
    keyword = MinimumLengthKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validation() -> None:
    # given
    document = {
        "minLength": 3,
    }
    keyword = MinimumLengthKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    schema.validate("abc")


def test_can_fail_validation() -> None:
    # given
    document = {
        "minLength": 3,
    }

    keyword = MinimumLengthKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(MinimumLengthValidationError) as e:
        schema.validate("1")

    # then
    assert e.value.expected_minimum == 3
    assert isinstance(e.value, LengthValidationError)
