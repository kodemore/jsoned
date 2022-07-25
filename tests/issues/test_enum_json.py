from jsoned import JsonSchema
from jsoned.vocabulary import DRAFT_2020_12_VOCABULARY


def test_heterogeneous_enum_array_is_valid() -> None:
    # given
    document = {'enum': [6, 'foo', [], True, {'foo': 12}]}
    data = []
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert schema.validate(data)


def test_enum_with_false_does_not_match_0() -> None:
    # given
    document = {'enum': [False]}
    data = False
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert schema.validate(data)
