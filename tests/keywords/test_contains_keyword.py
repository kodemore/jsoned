import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import ContainsKeyword, TypeKeyword
from jsoned.validators import Context


def test_can_instantiate() -> None:
    # given
    keyword = ContainsKeyword()

    # then
    assert isinstance(keyword, ContainsKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "contains": [],
    }
    keyword = ContainsKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validate() -> None:
    # given
    document = {
        "contains": {
            "type": "boolean"
        },
    }
    schema = JsonSchema(document, [ContainsKeyword(), TypeKeyword()])

    # then
    assert schema.validate([True])


def test_can_fail_validation() -> None:
    # given
    document = {
        "contains": {
            "type": "boolean"
        },
    }

    schema = JsonSchema(document, [ContainsKeyword(), TypeKeyword()])
    context = Context()

    # when
    assert not schema.validate(["a"], context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.ARRAY_MIN_CONTAINS_ERROR


