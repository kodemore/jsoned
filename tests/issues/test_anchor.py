from jsoned import JsonSchema, JsonStore
from jsoned.vocabulary import DRAFT_2020_12_VOCABULARY


def test_location_independent_identifier() -> None:
    # given
    document = {'$defs': {'A': {'$anchor': 'foo', 'type': 'integer'}}, '$ref': '#foo'}
    data = 1
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert schema.validate(data)


def test_location_independent_identifier_with_absolute_uri() -> None:
    # given
    document = {
        '$defs': {
            'A': {
                '$anchor': 'foo',
                '$id': 'http://localhost:1234/bar',
                'type': 'integer'
            }
        },
        '$ref': 'http://localhost:1234/bar#foo'
    }
    data = 1
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert schema.validate(data)


def test_nested_document_anchor_match() -> None:
    # given
    document = {
        '$defs': {
            'A': {
                '$defs': {
                    'B': {'$anchor': 'foo', 'type': 'integer'}
                },
                '$id': 'nested.json'
            }
        },
        '$id': 'http://localhost:1234/root',
        '$ref': 'http://localhost:1234/nested.json#foo'
    }

    data = 1
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # then
    assert schema.validate(data)


def test_ignore_anchor_inside_an_enum() -> None:
    # given
    document = {
        "$defs": {
            "anchor_in_enum": {
                "enum": [
                    {
                        "$anchor": "my_anchor",
                        "type": "null"
                    }
                ]
            },
            "real_identifier_in_schema": {
                "$anchor": "my_anchor",
                "type": "string"
            },
            "zzz_anchor_in_const": {
                "const": {
                    "$anchor": "my_anchor",
                    "type": "null"
                }
            }
        },
        "anyOf": [
            {"$ref": "#/$defs/anchor_in_enum"},
            {"$ref": "#my_anchor"}
        ]
    }
    data = {'type': 'null'}
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # when
    schema.load()

    # then
    assert not schema.validate(data)


def test_same_anchors_with_different_base_uris() -> None:
    # given
    document = {
        '$defs': {
            'A': {
                '$id': 'child1',
                'allOf': [{
                    '$anchor': 'my_anchor',
                    '$id': 'child2',
                    'type': 'number'
                }, {
                    '$anchor': 'my_anchor',
                    'type': 'string'
                }]
            }
        },
        '$id': 'http://localhost:1234/foobar',
        '$ref': 'child1#my_anchor'
    }
    data = "a"
    schema = JsonSchema(document, vocabulary=DRAFT_2020_12_VOCABULARY)

    # when
    schema.load()

    # then
    assert schema.validate(data)

