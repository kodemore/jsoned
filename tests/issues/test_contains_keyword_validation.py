from jsoned import JsonSchema
from jsoned.vocabulary import DRAFT_2020_12_VOCABULARY


def test_not_array_is_valid() -> None:
    # given
    document = {'contains': {'minimum': 5}}
    data = {}
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert schema.validate(data)


def test_non_empty_array_with_schema_true_is_valid() -> None:
    # given
    document = {'contains': True}
    data = ['foo']
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert schema.validate(data)


def test_matches_items_does_not_match_contains_should_fail() -> None:
    # given
    document = {'contains': {'multipleOf': 3}, 'items': {'multipleOf': 2}}
    data = [2, 4, 8]
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert not schema.validate(data)


def test_any_non_empty_array_is_valid_with_if_else() -> None:
    # given
    document = {'contains': {'else': True, 'if': False}}
    data = ['foo']
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert schema.validate(data)
