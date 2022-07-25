import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError
from jsoned.errors import ValidationError
from jsoned.keywords import FormatKeyword
from jsoned.validators import Context


def test_can_instantiate() -> None:
    # given
    keyword = FormatKeyword()

    # then
    assert isinstance(keyword, FormatKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "format": True,
    }
    keyword = FormatKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validate() -> None:
    # given
    document = {
        "format": "date-time",
    }
    keyword = FormatKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    assert schema.validate("2020-10-10T11:14:12")


def test_can_fail_validation() -> None:
    # given
    document = {
        "format": "date-time",
    }

    keyword = FormatKeyword()
    schema = JsonSchema(document, [keyword])
    context = Context()

    # when
    assert not schema.validate("abcd", context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.STRING_FORMAT_ERROR


