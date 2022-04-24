import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ContainsValidationError
from jsoned.keywords import ContainsKeyword, TypeKeyword


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

    # when
    schema.validate([True])


def test_can_fail_validation() -> None:
    # given
    document = {
        "contains": {
            "type": "boolean"
        },
    }

    schema = JsonSchema(document, [ContainsKeyword(), TypeKeyword()])

    # when
    with pytest.raises(ContainsValidationError) as e:
        schema.validate(["a"])
