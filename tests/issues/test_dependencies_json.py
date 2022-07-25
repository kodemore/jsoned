from jsoned import JsonSchema
from jsoned.vocabulary import DRAFT_2020_12_VOCABULARY


def test_dependencies_missing_dependency() -> None:
    # given
    document = {'dependencies': {'bar': ['foo']}}
    data = {'bar': 2}
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert not schema.validate(data)


def test_dependencies_ignores_arrays() -> None:
    # given
    document = {'dependencies': {'bar': ['foo']}}
    data = ['bar']
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert schema.validate(data)
