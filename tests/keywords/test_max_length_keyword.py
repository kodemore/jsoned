import pytest

from jsoned import JsonSchema
from jsoned.errors import MaximumLengthValidationError, LengthValidationError, SchemaParseError
from jsoned.keywords import MaximumLengthKeyword


def test_can_instantiate() -> None:
    # given
    keyword = MaximumLengthKeyword()

    # then
    assert isinstance(keyword, MaximumLengthKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "maxLength": True,
    }
    keyword = MaximumLengthKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validation() -> None:
    # given
    document = {
        "maxLength": 3,
    }
    keyword = MaximumLengthKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    schema.validate("abc")


def test_can_fail_validation() -> None:
    # given
    document = {
        "maxLength": 3,
    }

    keyword = MaximumLengthKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(MaximumLengthValidationError) as e:
        schema.validate("abcd")

    # then
    assert e.value.expected_maximum == 3
    assert isinstance(e.value, LengthValidationError)
