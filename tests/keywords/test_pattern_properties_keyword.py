import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import PatternPropertiesKeyword, TypeKeyword, FormatKeyword, PropertiesKeyword
from jsoned.validators import Context


def test_can_instantiate() -> None:
    # given
    keyword = PatternPropertiesKeyword()

    # then
    assert isinstance(keyword, PatternPropertiesKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "patternProperties": "abc",
    }
    keyword = PatternPropertiesKeyword()
    schema = JsonSchema(document, [keyword])

    # then
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validate() -> None:
    # given
    document = {
        "patternProperties": {
            "^S_": {"type": "string"},
            "^I_": {"type": "integer"},
        }
    }
    keywords = [PatternPropertiesKeyword(), TypeKeyword(), FormatKeyword()]
    schema = JsonSchema(document, keywords)

    # then
    assert schema.validate({
        "S_1": "Bob",
        "I_1": 20,
    })


def test_can_fail_validation() -> None:
    # given
    document = {
        "patternProperties": {
            "^S_": {"type": "string"},
            "^I_": {"type": "integer"},
        }
    }
    keywords = [PatternPropertiesKeyword(), TypeKeyword(), FormatKeyword()]
    schema = JsonSchema(document, keywords)
    context = Context()

    # when
    assert not schema.validate({
        "S_1": 123,
    }, context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.TYPE_ERROR
    assert context.errors[0].path == "S_1"


def test_can_work_with_properties() -> None:
    # given
    document = {
        "properties": {
            "S_0": {"type": "integer"}
        },
        "patternProperties": {
            "^S_": {"type": "string"},
            "^I_": {"type": "integer"},
        }
    }
    keywords = [PropertiesKeyword(), PatternPropertiesKeyword(), TypeKeyword(), FormatKeyword()]
    schema = JsonSchema(document, keywords)
    context = Context()

    # when
    assert schema.validate({
        "S_0": 123,
        "S_1": "string",
        "I_0": 123,
    })

    # when
    assert not schema.validate({
            "S_0": "abc",
            "S_1": "string",
            "I_0": 123,
    }, context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.TYPE_ERROR
    assert context.errors[0].path == "S_0"

