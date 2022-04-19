import pytest

from jsoned import JsonSchema
from jsoned.errors import TypeValidationError, SchemaParseError
from jsoned.keywords import TypeKeyword


def test_can_instantiate() -> None:
    # given
    keyword = TypeKeyword()

    # then
    assert isinstance(keyword, TypeKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "type": "unknown",
    }
    keyword = TypeKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validate() -> None:
    # given
    document = {
        "type": "boolean"
    }
    keyword = TypeKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    schema.validate(True)


def test_can_fail_validation() -> None:
    # given
    document = {
        "type": "boolean"
    }
    keyword = TypeKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(TypeValidationError) as e:
        schema.validate("1")

        # then
        assert e.context.get("expected_type") == "boolean"
        assert e.context.get("passed_type") == "string"
        assert e.path == "/type"
