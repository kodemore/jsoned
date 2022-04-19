from os import path

from jsoned import JsonSchema, JsonStore, MappableUriResolver
from jsoned.keywords import RefKeyword
from jsoned.keywords.ref_keyword import JsonReference


def test_can_resolve_local_ref() -> None:
    # given
    json_data = {
        "properties": {
            "name": {
                "$ref": "#/defs/generic_name",
            },
            "last_name": {
                "$ref": "#/defs/generic_name",
            },
            "email": {
                "type": "string",
            },
        },
        "defs": {
            "generic_name": {
                "type": "string",
            }
        },
    }
    store = JsonStore.default()
    ref_keyword = RefKeyword(store)
    schema = JsonSchema(json_data, [ref_keyword])

    # when
    node = schema.query("/properties/name")

    # then
    assert isinstance(node, JsonReference)
    assert node == {"type": "string"}


def test_can_resolve_local_ref_to_primitive_value() -> None:
    # given
    json_data = {
        "properties": {
            "name": {
                "type": {
                    "$ref": "#/defs/generic_name/type",
                }
            },
        },
        "defs": {
            "generic_name": {
                "type": "string",
            }
        },
    }
    store = JsonStore.default()
    ref_keyword = RefKeyword(store)
    schema = JsonSchema(json_data, [ref_keyword])

    # when
    node = schema.query("/properties/name/type")

    # then
    assert isinstance(node, JsonReference)
    assert node == "string"


def test_can_resolve_recursive_ref() -> None:
    # given
    json_data = {
        "properties": {
            "name": {
                "type": "string",
            },
            "$ref": "#",
        },
    }
    store = JsonStore.default()
    ref_keyword = RefKeyword(store)
    schema = JsonSchema(json_data, [ref_keyword])

    # when
    value = schema.query("/properties/properties/properties/name/type")

    # then
    assert value == "string"


def test_can_resolve_non_local_ref() -> None:
    # given
    json_data = {
        "properties": {
            "name": {
                "type": "string",
            },
            "$ref": "file://schema_plain.json#/0/schema",
        },
    }
    dir_name = path.dirname(__file__)

    store = JsonStore.default()

    resolver = MappableUriResolver()
    resolver.map("file://", path.join(dir_name, "..", "fixtures"))

    store.loader.register("file", resolver)

    ref_keyword = RefKeyword(store)
    schema = JsonSchema(json_data, [ref_keyword])

    # when
    ref_a = schema.query("/properties/name/type")
    ref_b = schema.query("/properties/items/type")

    # then
    assert ref_a == "string"
    assert ref_b == "integer"

