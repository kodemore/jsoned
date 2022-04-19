import pytest

from jsoned import JsonSchema, JsonStore
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import PropertiesKeyword, TypeKeyword, FormatKeyword, RefKeyword


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

    # when
    schema.validate({
        "name": "Bob",
        "email": "bob@builder.com",
    })

    # then
    assert "properties" in schema.validator
    assert "name" in schema.validator["properties"]
    assert "email" in schema.validator["properties"]
    assert "type" in schema.validator["properties"]["name"]
    assert "type" in schema.validator["properties"]["email"]
    assert "format" in schema.validator["properties"]["email"]


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

    # when
    with pytest.raises(ValidationError) as e:
        schema.validate("1")

    assert e.value.path == ""

    # when
    with pytest.raises(ValidationError) as e:
        schema.validate({"email": "invalid"})

    assert e.value.path == ".email@format"


def test_can_pass_ref_validation() -> None:
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
    schema.load()
    schema.validate({"extra": {"extra": {"email": 1}}})
