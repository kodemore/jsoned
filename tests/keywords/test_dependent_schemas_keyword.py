import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import DependentSchemasKeyword, TypeKeyword, PropertiesKeyword, RequiredPropertiesKeyword
from jsoned.validators import Context


def test_can_instantiate() -> None:
    # given
    keyword = DependentSchemasKeyword()

    # then
    assert isinstance(keyword, DependentSchemasKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "dependentSchemas": [],
    }
    keyword = DependentSchemasKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validate() -> None:
    # given
    document = {
        "type": "object",

        "properties": {
            "name": {"type": "string"},
            "credit_card": {"type": "number"}
        },

        "required": ["name"],

        "dependentSchemas": {
            "credit_card": {
                "properties": {
                    "billing_address": {"type": "string"}
                },
                "required": ["billing_address"]
            }
        }
    }
    schema = JsonSchema(
        document,
        [DependentSchemasKeyword(), TypeKeyword(), PropertiesKeyword(), RequiredPropertiesKeyword()]
    )

    # then
    assert schema.validate({
        "name": "John Doe",
        "credit_card": 5555555555555555,
        "billing_address": "555 Debtor's Lane"
    })

    assert schema.validate({
        "name": "John Doe",
        "billing_address": "555 Debtor's Lane"
    })


def test_can_fail_validation() -> None:
    # given
    document = {
        "type": "object",

        "properties": {
            "name": {"type": "string"},
            "credit_card": {"type": "number"}
        },

        "required": ["name"],

        "dependentSchemas": {
            "credit_card": {
                "properties": {
                    "billing_address": {"type": "string"}
                },
                "required": ["billing_address"]
            }
        }
    }
    schema = JsonSchema(
        document,
        [DependentSchemasKeyword(), TypeKeyword(), PropertiesKeyword(), RequiredPropertiesKeyword()]
    )
    context = Context()

    # when
    assert not schema.validate({
        "name": "John Doe",
        "credit_card": 5555555555555555
    }, context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.PROPERTY_MISSING_ERROR
