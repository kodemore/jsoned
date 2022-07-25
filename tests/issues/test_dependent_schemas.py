from jsoned import JsonSchema
from jsoned.vocabulary import DRAFT_2020_12_VOCABULARY


def test_ignores_other_non_objects() -> None:
    # given
    document = {'dependentSchemas': {'bar': {'properties': {'bar': {'type': 'integer'}, 'foo': {'type': 'integer'}}}}}
    data = 12
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert schema.validate(data)
