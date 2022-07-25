from jsoned import JsonSchema
from jsoned.vocabulary import DRAFT_2020_12_VOCABULARY


def test_regex_is_not_anchored_and_case_sensitive() -> None:
    # given
    document = {'patternProperties': {'X_': {'type': 'string'}, '[0-9]{2,}': {'type': 'boolean'}}}
    data = {'a31b': None}
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert not schema.validate(data)
