import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import DependentSchemasKeyword, TypeKeyword, PropertiesKeyword, RequiredPropertiesKeyword


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

    # when
    schema.validate({
        "name": "John Doe",
        "credit_card": 5555555555555555,
        "billing_address": "555 Debtor's Lane"
    })

    schema.validate({
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

        "patternProperties": {
            ...,
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

    # when
    with pytest.raises(ValidationError) as e:
        schema.validate({
            "name": "John Doe",
            "credit_card": 5555555555555555
        })
