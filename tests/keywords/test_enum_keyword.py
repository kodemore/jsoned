import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError
from jsoned.errors import ValidationError
from jsoned.keywords import EnumKeyword
from jsoned.validators import Context


def test_can_instantiate() -> None:
    # given
    keyword = EnumKeyword()

    # then
    assert isinstance(keyword, EnumKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "enum": True,
    }
    keyword = EnumKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validate() -> None:
    # given
    document = {
        "enum": ["a", 1],
    }
    keyword = EnumKeyword()
    schema = JsonSchema(document, [keyword])

    # then
    assert schema.validate("a")
    assert schema.validate(1)


def test_can_fail_validation() -> None:
    # given
    document = {
        "enum": ["a", 1],
    }

    keyword = EnumKeyword()
    schema = JsonSchema(document, [keyword])
    context = Context()

    # when
    assert not schema.validate(True, context)

    # then
    assert len(context.errors) == 1
    assert context.errors[0].code == ValidationError.ErrorCodes.ENUM_ERROR

