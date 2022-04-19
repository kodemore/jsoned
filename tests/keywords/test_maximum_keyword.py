import pytest

from jsoned import JsonSchema
from jsoned.errors import MaximumValidationError, SchemaParseError
from jsoned.keywords import MaximumKeyword


def test_can_instantiate() -> None:
    # given
    keyword = MaximumKeyword()

    # then
    assert isinstance(keyword, MaximumKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "maximum": True,
    }
    keyword = MaximumKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validation() -> None:
    # given
    document = {
        "maximum": 100,
    }
    keyword = MaximumKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    schema.validate(0)
    schema.validate(1)
    schema.validate(20)


def test_can_fail_validation() -> None:
    # given
    document = {
        "maximum": 100,
    }

    keyword = MaximumKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(MaximumValidationError) as e:
        schema.validate(101)

    # then
    assert e.value.expected_maximum == 100


def test_can_be_used_with_exclusive_minimum() -> None:
    # given
    document = {
        "maximum": 100,
        "exclusiveMaximum": True,
    }

    keyword = MaximumKeyword()
    schema = JsonSchema(document, [keyword])

    # then
    schema.validate(10)
    schema.validate(20)

    # when
    with pytest.raises(MaximumValidationError) as e:
        schema.validate(100)

    # then
    assert e.value.expected_maximum == 100
