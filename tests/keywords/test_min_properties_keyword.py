import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError
from jsoned.errors.object_validation_errors import MinimumPropertiesValidationError
from jsoned.keywords import MinimumPropertiesKeyword


def test_can_instantiate() -> None:
    # given
    keyword = MinimumPropertiesKeyword()

    # then
    assert isinstance(keyword, MinimumPropertiesKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "minProperties": True,
    }
    keyword = MinimumPropertiesKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validation() -> None:
    # given
    document = {
        "minProperties": 2,
    }
    keyword = MinimumPropertiesKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    schema.validate({"a": 1, "b": 2})


def test_can_fail_validation() -> None:
    # given
    document = {
        "minProperties": 2,
    }

    keyword = MinimumPropertiesKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(MinimumPropertiesValidationError) as e:
        schema.validate({"a": 1})

    # then
    assert e.value.expected_minimum == 2
