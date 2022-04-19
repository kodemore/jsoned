import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError
from jsoned.errors.string_validation_errors import FormatValidationError
from jsoned.keywords import PatternKeyword


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

    # when
    schema.validate("555-1212")
    schema.validate("(888)555-1212")


def test_can_fail_validation() -> None:
    # given
    document = {
        "type": "string",
        "pattern": "^(\\([0-9]{3}\\))?[0-9]{3}-[0-9]{4}$"
    }

    keyword = PatternKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(FormatValidationError) as e:
        schema.validate("(888)555-1212 ext. 532")

    # then
    assert e.value.expected_format == document["pattern"]

    # when
    with pytest.raises(FormatValidationError):
        schema.validate("(800)FLOWERS")
