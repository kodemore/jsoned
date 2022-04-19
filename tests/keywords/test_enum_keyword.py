import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError
from jsoned.errors import EnumValidationError
from jsoned.keywords import EnumKeyword


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

    # when
    schema.validate("a")
    schema.validate(1)


def test_can_fail_validation() -> None:
    # given
    document = {
        "enum": ["a", 1],
    }

    keyword = EnumKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(EnumValidationError) as e:
        schema.validate(True)

    # then
    assert e.value.expected_values == ["a", 1]

