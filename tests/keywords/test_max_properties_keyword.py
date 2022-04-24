import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError
from jsoned.errors.object_validation_errors import MaximumPropertiesValidationError
from jsoned.keywords import MaximumPropertiesKeyword


def test_can_instantiate() -> None:
    # given
    keyword = MaximumPropertiesKeyword()

    # then
    assert isinstance(keyword, MaximumPropertiesKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "maxProperties": True,
    }
    keyword = MaximumPropertiesKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validation() -> None:
    # given
    document = {
        "maxProperties": 2,
    }
    keyword = MaximumPropertiesKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    schema.validate({"a": 1, "b": 2})


def test_can_fail_validation() -> None:
    # given
    document = {
        "maxProperties": 2,
    }

    keyword = MaximumPropertiesKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(MaximumPropertiesValidationError) as e:
        schema.validate({"a": 1, "b": 2, "c": 3})

    # then
    assert e.value.expected_maximum == 2
