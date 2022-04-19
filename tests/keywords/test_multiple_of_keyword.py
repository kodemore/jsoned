import pytest

from jsoned import JsonSchema
from jsoned.errors import MultipleOfValidationError, SchemaParseError
from jsoned.keywords import MultipleOfKeyword


def test_can_instantiate() -> None:
    # given
    keyword = MultipleOfKeyword()

    # then
    assert isinstance(keyword, MultipleOfKeyword)


def test_fail_to_parse() -> None:
    # given
    document = {
        "multipleOf": True,
    }
    keyword = MultipleOfKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(SchemaParseError):
        _ = schema.validate("abc")


def test_can_pass_validation() -> None:
    # given
    document = {
        "multipleOf": 10,
    }
    keyword = MultipleOfKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    schema.validate(0)
    schema.validate(10)
    schema.validate(20)


def test_can_fail_validation() -> None:
    # given
    document = {
        "multipleOf": 10,
    }

    keyword = MultipleOfKeyword()
    schema = JsonSchema(document, [keyword])

    # when
    with pytest.raises(MultipleOfValidationError) as e:
        schema.validate(23)

    # then
    assert e.value.multiple_of == 10
