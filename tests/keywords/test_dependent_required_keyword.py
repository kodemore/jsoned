import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import DependentRequiredKeyword
from jsoned.validators import Context


def test_can_instantiate() -> None:
    # given
    keyword = DependentRequiredKeyword()

    # then
    assert isinstance(keyword, DependentRequiredKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "dependentRequired": [],
    }
    keyword = DependentRequiredKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validate() -> None:
    # given
    document = {
        "dependentRequired": {
            "credit_card": ["billing_address"]
        }
    }
    schema = JsonSchema(document, [DependentRequiredKeyword()])

    # when
    assert schema.validate({"a": 1})
    assert schema.validate({"credit_card": "number", "billing_address": "address"})


def test_can_fail_validation() -> None:
    # given
    document = {
        "dependentRequired": {
            "credit_card": ["billing_address"]
        }
    }

    schema = JsonSchema(document, [DependentRequiredKeyword()])
    context = Context()

    # when
    assert not schema.validate({"credit_card": "number"}, context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.PROPERTY_MISSING_ERROR
