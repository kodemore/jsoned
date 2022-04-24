import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ConstValidationError
from jsoned.keywords import ConstKeyword


def test_can_instantiate() -> None:
    # given
    keyword = ConstKeyword()

    # then
    assert isinstance(keyword, ConstKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "const": [],
    }
    keyword = ConstKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validate() -> None:
    # given
    document = {
        "const": True,
    }
    keyword = ConstKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    schema.validate(True)


def test_can_fail_validation() -> None:
    # given
    document = {
        "const": True,
    }

    keyword = ConstKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(ConstValidationError) as e:
        schema.validate(1)

    # then
    assert e.value.expected_value == True

