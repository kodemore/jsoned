import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import NotKeyword, TypeKeyword
from jsoned.validators import Context


def test_can_instantiate() -> None:
    # given
    keyword = NotKeyword()

    # then
    assert isinstance(keyword, NotKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "not": 12,
    }
    keyword = NotKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validate() -> None:
    # given
    document = {
        "not": {"type": "string"},
    }
    schema = JsonSchema(document, [NotKeyword(), TypeKeyword()])

    # then
    assert schema.validate(False)
    assert schema.validate(12)


def test_can_fail_validation() -> None:
    # given
    document = {
        "not": {"type": "string"},
    }
    schema = JsonSchema(document, [NotKeyword(), TypeKeyword()])
    context = Context()

    # when
    assert not schema.validate("a", context)
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.NOT_ERROR

