import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import ConstKeyword
from jsoned.validators import Context


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

    # then
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validate() -> None:
    # given
    document = {
        "const": True,
    }
    keyword = ConstKeyword()
    schema = JsonSchema(document, [keyword])

    # then
    schema.validate(True)


def test_can_fail_validation() -> None:
    # given
    document = {
        "const": True,
    }

    keyword = ConstKeyword()
    schema = JsonSchema(document, [keyword])
    context = Context()

    # when
    assert not schema.validate(1, context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.EQUAL_ERROR

