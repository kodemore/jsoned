import pytest

from jsoned import JsonSchema
from jsoned.errors import MinimumValidationError, SchemaParseError
from jsoned.keywords import MinimumKeyword


def test_can_instantiate() -> None:
    # given
    keyword = MinimumKeyword()

    # then
    assert isinstance(keyword, MinimumKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "minimum": True,
    }
    keyword = MinimumKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validation() -> None:
    # given
    document = {
        "minimum": 0,
    }
    keyword = MinimumKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    schema.validate(0)
    schema.validate(1)
    schema.validate(20)


def test_can_fail_validation() -> None:
    # given
    document = {
        "minimum": 0,
    }

    keyword = MinimumKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(MinimumValidationError) as e:
        schema.validate(-1)

    # then
    assert e.value.expected_minimum == 0


def test_can_be_used_with_exclusive_minimum() -> None:
    # given
    document = {
        "minimum": 0,
        "exclusiveMinimum": True,
    }

    keyword = MinimumKeyword()
    schema = JsonSchema(document, [keyword])

    # then
    schema.validate(1)
    schema.validate(2)

    # when
    with pytest.raises(MinimumValidationError) as e:
        schema.validate(0)

    # then
    assert e.value.expected_minimum == 0
