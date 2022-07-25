import pytest

from jsoned import JsonSchema
from jsoned.errors import SchemaParseError, ValidationError
from jsoned.keywords import ConstKeyword
from jsoned.validators import Context
from jsoned.vocabulary import DRAFT_2020_12_VOCABULARY


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


def test_const_with_object_same_object_is_valid() -> None:
    # given
    document = {'const': {'baz': 'bax', 'foo': 'bar'}}
    data = {'baz': 'bax', 'foo': 'bar'}
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert schema.validate(data)


def test_const_with_false_does_not_match_0() -> None:
    # given
    document = {'const': False}
    data = 0
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert not schema.validate(data)
