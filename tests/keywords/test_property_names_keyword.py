import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import PropertyNamesKeyword, TypeKeyword, PatternKeyword
from jsoned.validators import Context


def test_can_instantiate() -> None:
    # given
    keyword = PropertyNamesKeyword()

    # then
    assert isinstance(keyword, PropertyNamesKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "propertyNames": "abc",
    }
    keyword = PropertyNamesKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validate() -> None:
    # given
    document = {
        "propertyNames": {
            "pattern": "^an?_"
        }
    }
    keywords = [PropertyNamesKeyword(), PatternKeyword()]
    schema = JsonSchema(document, keywords)

    # then
    assert schema.validate({
        "a_name": "Bob",
        "an_email": "bob@builder.com",
    })


def test_can_fail_validation() -> None:
    # given
    document = {
        "propertyNames": {
            "pattern": "^an?_"
        }
    }
    keywords = [PropertyNamesKeyword(), PatternKeyword()]
    schema = JsonSchema(document, keywords)
    context = Context()

    # when
    assert not schema.validate({"email": "invalid"}, context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.PROPERTY_INVALID_NAME_ERROR
