import pytest

from jsoned import JsonSchema
from jsoned.errors import MinimumValidationError, SchemaParseError
from jsoned.keywords import ExclusiveMinimumKeyword


def test_can_instantiate() -> None:
    # given
    keyword = ExclusiveMinimumKeyword()

    # then
    assert isinstance(keyword, ExclusiveMinimumKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "exclusiveMinimum": True,
    }
    keyword = ExclusiveMinimumKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validation() -> None:
    # given
    document = {
        "exclusiveMinimum": 0,
    }
    keyword = ExclusiveMinimumKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    schema.validate(1)
    schema.validate(20)


def test_can_fail_validation() -> None:
    # given
    document = {
        "exclusiveMinimum": 0,
    }

    keyword = ExclusiveMinimumKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(MinimumValidationError) as e:
        schema.validate(0)

    # then
    assert e.value.expected_minimum == 0
