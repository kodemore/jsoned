from jsoned import JsonSchema
from jsoned.vocabulary import DRAFT_2020_12_VOCABULARY


def test_can_ignore_if_without_then_else() -> None:
    # given
    document = {'if': {'const': 0}}
    data = "hello"
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert schema.validate(data)


def test_valid_when_if_test_fails() -> None:
    # given
    document = {'if': {'exclusiveMaximum': 0}, 'then': {'minimum': -10}}
    data = 3
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert schema.validate(data)
