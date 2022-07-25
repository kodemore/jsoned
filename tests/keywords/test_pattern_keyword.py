import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError
from jsoned.errors import ValidationError
from jsoned.keywords import PatternKeyword
from jsoned.validators import Context


def test_can_instantiate() -> None:
    # given
    keyword = PatternKeyword()

    # then
    assert isinstance(keyword, PatternKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "pattern": True,
    }
    keyword = PatternKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validation() -> None:
    # given
    document = {
       "type": "string",
       "pattern": "^(\\([0-9]{3}\\))?[0-9]{3}-[0-9]{4}$"
    }

    keyword = PatternKeyword()
    schema = JsonSchema(document, [keyword])

    # then
    assert schema.validate("555-1212")
    assert schema.validate("(888)555-1212")


def test_can_fail_validation() -> None:
    # given
    document = {
        "type": "string",
        "pattern": "^(\\([0-9]{3}\\))?[0-9]{3}-[0-9]{4}$"
    }

    keyword = PatternKeyword()
    schema = JsonSchema(document, [keyword])
    context = Context()

    # when
    assert not schema.validate("(888)555-1212 ext. 532", context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.STRING_PATTERN_ERROR

    # when
    context = Context()
    assert not schema.validate("(800)FLOWERS", context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.STRING_PATTERN_ERROR
