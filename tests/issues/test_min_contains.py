from jsoned import JsonSchema
from jsoned.vocabulary import DRAFT_2020_12_VOCABULARY


def test_min_contains_0() -> None:
    # given
    document = {'contains': {'const': 1}, 'minContains': 0}
    data = []
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert schema.validate(data)
