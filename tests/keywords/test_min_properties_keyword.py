import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError
from jsoned.errors import ValidationError
from jsoned.keywords import MinimumPropertiesKeyword
from jsoned.validators import Context


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
    assert schema.validate({"a": 1, "b": 2})


def test_can_fail_validation() -> None:
    # given
    document = {
        "minProperties": 2,
    }

    keyword = MinimumPropertiesKeyword()
    schema = JsonSchema(document, [keyword])
    context = Context()

    # when
    assert not schema.validate({"a": 1}, context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.PROPERTY_MINIMUM_LENGTH_ERROR
