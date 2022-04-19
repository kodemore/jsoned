import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, MaximumValidationError
from jsoned.keywords import ExclusiveMaximumKeyword


def test_can_instantiate() -> None:
    # given
    keyword = ExclusiveMaximumKeyword()

    # then
    assert isinstance(keyword, ExclusiveMaximumKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "exclusiveMaximum": True,
    }
    keyword = ExclusiveMaximumKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validation() -> None:
    # given
    document = {
        "exclusiveMaximum": 10,
    }
    keyword = ExclusiveMaximumKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    schema.validate(1)
    schema.validate(9)


def test_can_fail_validation() -> None:
    # given
    document = {
        "exclusiveMaximum": 10,
    }

    keyword = ExclusiveMaximumKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(MaximumValidationError) as e:
        schema.validate(10)

    # then
    assert e.value.expected_maximum == 10
