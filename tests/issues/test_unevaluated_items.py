from jsoned import JsonSchema
from jsoned.validators import Context
from jsoned.vocabulary import DRAFT_2020_12_VOCABULARY, CORE_VOCABULARY


def test_allow_unevaluated_items() -> None:
    # given
    document = {'type': 'array', 'unevaluatedItems': True}
    data = ['foo']
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert schema.validate(data)


def test_allow_unevaluated_items_that_match_validator() -> None:
    # given
    document = {'type': 'array', 'unevaluatedItems': {'type': 'string'}}
    data = ['foo']
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert schema.validate(data)


def test_disallow_unevaluated_items() -> None:
    # given
    document = {'prefixItems': [{'type': 'string'}], 'type': 'array', 'unevaluatedItems': False}
    data = ['foo', 'bar']
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)
    context = Context()

    # then
    assert not schema.validate(data, context)


def test_unevaluated_items_does_not_apply() -> None:
    # given
    document = {'items': True, 'prefixItems': [{'type': 'string'}], 'type': 'array', 'unevaluatedItems': False}
    data = ['foo', 42]
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    context = Context()
    assert schema.validate(data, context)


def test_unevaluated_items_with_nested_tuple() -> None:
    # given
    document = {'allOf': [{'prefixItems': [True, {'type': 'number'}]}], 'prefixItems': [{'type': 'string'}], 'type': 'array', 'unevaluatedItems': False}
    data = ['foo', 42]
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    context = Context()
    assert schema.validate(data, context)


def test_unevaluated_items_with_additional_items() -> None:
    # given
    document = {'allOf': [{'items': True, 'prefixItems': [{'type': 'string'}]}], 'type': 'array', 'unevaluatedItems': False}
    data = ['foo', 42, True]
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    context = Context()
    assert schema.validate(data, context)


def test_unevaluated_items_with_any_of() -> None:
    # given
    document = {
        'anyOf': [
            {'prefixItems': [True, {'const': 'bar'}]},
            {'prefixItems': [True, True, {'const': 'baz'}]}
        ],
        'prefixItems': [{'const': 'foo'}],
        'type': 'array',
        'unevaluatedItems': False
    }
    data = ['foo', 'bar']
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    context = Context()
    assert schema.validate(data, context)


def test_when_no_schema_matches_and_has_unevaluated_items() -> None:
    # given
    document = {
        'anyOf': [
            {'prefixItems': [True, {'const': 'bar'}]},
            {'prefixItems': [True, True, {'const': 'baz'}]}
        ],
        'prefixItems': [{'const': 'foo'}],
        'type': 'array',
        'unevaluatedItems': False
    }

    data = ['foo', 'bar', 42]
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    context = Context()
    assert not schema.validate(data, context)


def test_with_not_and_unevaluated_items() -> None:
    # given
    document = {
        'not': {
            'not': {
                'prefixItems': [
                    True,
                    {'const': 'bar'}
                ]
            }
        },
        'prefixItems': [{'const': 'foo'}],
        'type': 'array',
        'unevaluatedItems': False,
    }

    data = ['foo', 'bar', 42]
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    context = Context()
    assert not schema.validate(data, context)


def test_ref_with_no_unevaluated_items() -> None:
    # given
    document = {
        "type": "array",
        "$ref": "#/$defs/bar",
        "prefixItems": [
            { "type": "string" }
        ],
        "unevaluatedItems": False,
        "$defs": {
          "bar": {
              "prefixItems": [
                  True,
                  { "type": "string" }
              ]
          }
        }
    }
    data = ["foo", "bar"]
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert schema.validate(data)


def test_contains_allowed_unevaluated_items() -> None:
    # given
    document = {'allOf': [{'contains': {'multipleOf': 2}}, {'contains': {'multipleOf': 3}}], 'unevaluatedItems': {'multipleOf': 5}}
    data = [2, 3, 4, 5, 6]
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert schema.validate(data)
