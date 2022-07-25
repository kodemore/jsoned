from jsoned import JsonSchema
from jsoned.validators import Context
from jsoned.vocabulary import DRAFT_2020_12_VOCABULARY


def test_ignores_non_arrays() -> None:
    # given
    document = {'items': {'type': 'integer'}}
    data = {'foo': 'bar'}
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert schema.validate(data)


def test_javascript_pseudo_array_is_valid() -> None:
    # given
    document = {'items': [{'type': 'integer'}, {'type': 'string'}]}
    data = {'0': 'invalid', '1': 'valid', 'length': 2}
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert schema.validate(data)


def test_any_non_empty_array_is_invalid() -> None:
    # given
    document = {'items': False}
    data = [1, 'foo', True]
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert not schema.validate(data)


def test_prefix_items_in_all_of_should_not_constrain_items() -> None:
    # given
    document = {
        'allOf': [
            {
                'prefixItems': [{'minimum': 3}]
            }
        ],
        'items': {'minimum': 5}
    }

    data = [5, 5]
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    schema.validate(data, context := Context())

    a = 1


def test_valid_items_and_subitems() -> None:
    # given
    document = {
        "$defs": {
            "item": {
                "type": "array",
                "items": False,
                "prefixItems": [
                    {"$ref": "#/$defs/sub-item"},
                    {"$ref": "#/$defs/sub-item"}
                ]
            },
            "sub-item": {
                "type": "object",
                "required": ["foo"]
            }
        },
        "type": "array",
        "items": False,
        "prefixItems": [
            {"$ref": "#/$defs/item"},
            {"$ref": "#/$defs/item"},
            {"$ref": "#/$defs/item"}
        ]
    }
    data = [
        [{'foo': None}, {'foo': None}],
        [{'foo': None}, {'foo': None}],
        [{'foo': None}, {'foo': None}]
    ]
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert schema.validate(data)
