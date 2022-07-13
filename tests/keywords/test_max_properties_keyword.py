import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError
from jsoned.errors import ValidationError
from jsoned.keywords import MaximumPropertiesKeyword
from jsoned.validators import Context


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

    # then
    assert schema.validate({"a": 1, "b": 2})


def test_can_fail_validation() -> None:
    # given
    document = {
        "maxProperties": 2,
    }

    keyword = MaximumPropertiesKeyword()
    schema = JsonSchema(document, [keyword])
    context = Context()

    # when
    assert not schema.validate({"a": 1, "b": 2, "c": 3}, context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.PROPERTY_MAXIMUM_LENGTH_ERROR
