from jsoned import JsonSchema
from jsoned.vocabulary import DRAFT_2020_12_VOCABULARY


def test_exclusive_minimum_validation_boundary_point_is_invalid() -> None:
    # given
    document = {'exclusiveMinimum': 1.1}
    data = 1.1
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert not schema.validate(data)
