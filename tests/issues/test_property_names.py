from jsoned import JsonSchema
from jsoned.vocabulary import DRAFT_2020_12_VOCABULARY


def test_boolean_true_always_passes() -> None:
    # given
    document = {'propertyNames': True}
    data = {'foo': 1}
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert schema.validate(data)


def test_pattern_additional_properties_interaction() -> None:
    # given
    document = {
        'additionalProperties': {'type': 'integer'},
        'patternProperties': {'f.o': {'minItems': 2}},
        'properties': {
            'bar': {'type': 'array'},
            'foo': {'maxItems': 3, 'type': 'array'}
        }
    }
    data = {'foo': []}
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert not schema.validate(data)
