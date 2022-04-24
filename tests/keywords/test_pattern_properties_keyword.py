import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import PatternPropertiesKeyword, TypeKeyword, FormatKeyword, PropertiesKeyword


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

    # when
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

    # when
    schema.validate({
        "S_1": "Bob",
        "I_1": 20,
    })

    # then
    assert "properties" in schema.validator
    assert "^S_" in schema.validator["properties"].pattern_properties
    assert "^I_" in schema.validator["properties"].pattern_properties


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

    # when
    with pytest.raises(ValidationError) as e:
        schema.validate({
            "S_1": 123,
        })

    # then
    error = e.value
    assert error.path == "S_1"


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

    # when
    schema.validate({
        "S_0": 123,
        "S_1": "string",
        "I_0": 123,
    })

    # when
    with pytest.raises(ValidationError) as e:
        schema.validate({
            "S_0": "abc",
            "S_1": "string",
            "I_0": 123,
        })
    error = e.value

    assert error.path == "S_0"
