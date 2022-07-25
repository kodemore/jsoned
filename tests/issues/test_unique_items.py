from jsoned import JsonSchema
from jsoned.vocabulary import DRAFT_2020_12_VOCABULARY


def test_false_is_not_equal_to_zero() -> None:
    # given
    document = {'uniqueItems': True}
    data = [0, False]
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert schema.validate(data)

