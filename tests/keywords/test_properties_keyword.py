import pytest

from jsoned import JsonSchema, JsonStore
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import PropertiesKeyword, TypeKeyword, FormatKeyword, RefKeyword
from jsoned.validators import Context


def test_can_instantiate() -> None:
    # given
    keyword = PropertiesKeyword()

    # then
    assert isinstance(keyword, PropertiesKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "properties": "abc",
    }
    keyword = PropertiesKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validate() -> None:
    # given
    document = {
        "properties": {
            "name": {
                "type": "string",
            },
            "email": {
                "type": "string",
                "format": "email",
            }
        }
    }
    keywords = [PropertiesKeyword(), TypeKeyword(), FormatKeyword()]
    schema = JsonSchema(document, keywords)

    # then
    assert schema.validate({
        "name": "Bob",
        "email": "bob@builder.com",
    })


def test_can_fail_validation() -> None:
    # given
    document = {
        "properties": {
            "name": {
                "type": "string",
            },
            "email": {
                "type": "string",
                "format": "email",
            }
        }
    }
    keywords = [PropertiesKeyword(), TypeKeyword(), FormatKeyword()]
    schema = JsonSchema(document, keywords)
    context = Context()

    # when
    assert not schema.validate({"email": "invalid"}, context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.STRING_FORMAT_ERROR
    assert context.errors[0].path == "email"


def test_fails_ref_validation() -> None:
    # given
    document = {
        "properties": {
            "name": {
                "type": "string",
            },
            "email": {
                "type": "string",
                "format": "email",
            },
            "extra": {
                "$ref": "#/"
            }
        }
    }
    store = JsonStore.default()
    keywords = [PropertiesKeyword(), TypeKeyword(), FormatKeyword(), RefKeyword(store)]
    schema = JsonSchema(document, keywords)
    context = Context()

    # when
    assert not schema.validate({"extra": {"extra": {"email": 1}}}, context)

    # then
    assert len(context.errors) == 2
    assert context.errors[0].path == "extra.extra.email"
    assert context.errors[1].path == "extra.extra.email"


def test_passes_ref_validation() -> None:
    # given
    document = {
        "properties": {
            "name": {
                "type": "string",
            },
            "email": {
                "type": "string",
                "format": "email",
            },
            "extra": {
                "$ref": "#/"
            }
        }
    }
    store = JsonStore.default()
    keywords = [PropertiesKeyword(), TypeKeyword(), FormatKeyword(), RefKeyword(store)]
    schema = JsonSchema(document, keywords)

    # then
    assert schema.validate({"extra": {"extra": {"email": "test@email.com"}}})
