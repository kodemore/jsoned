from jsoned import JsonDocument, JsonStore
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
    doc = JsonDocument(json_data, [ref_keyword])

    # when
    value = doc.value

    # then
    assert isinstance(value["properties"]["name"], JsonReference)
    assert value["properties"]["name"] == {"type": "string"}


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
    doc = JsonDocument(json_data, [ref_keyword])

    # when
    value = doc.value

    # then
    assert str(value["properties"]["name"]["type"]) == "string"


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
    doc = JsonDocument(json_data, [ref_keyword])

    # when
    value = doc.value

    # then
    assert value["properties"]["properties"]["properties"]["name"]["type"] == "string"


def test_can_resolve_non_local_ref() -> None:
    ...
