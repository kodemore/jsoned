from jsoned import JsonSchema, Uri, JsonStore
from jsoned.keywords import IdKeyword


def test_can_instantiate() -> None:
    # given
    keyword = IdKeyword(JsonStore.default())

    # then
    assert isinstance(keyword, IdKeyword)


def test_can_use_id_without_dollar_sign() -> None:
    # given
    keyword = IdKeyword(JsonStore.default())
    json = {"id": "https://test.com/document-id", "properties": {"a": 1, "b": 2}}
    document = JsonSchema(json, [keyword])

    # when
    document.load()

    # then
    assert document.id == "https://test.com/document-id"
    assert isinstance(document.id, Uri)
    assert document.id in JsonStore.default()


def test_can_use_id_with_dollar_sign() -> None:
    # given
    keyword = IdKeyword(JsonStore.default())
    json = {"$id": "https://test.com/document-id", "properties": {"a": 1, "b": 2}}
    document = JsonSchema(json, [keyword])

    # when
    document.load()

    # then
    assert document.id == "https://test.com/document-id"
    assert document.id in JsonStore.default()


def test_can_bundle_schemas() -> None:
    # given
    json = {
        "$id": "https://example.com/schemas/customer",
        "$schema": "https://json-schema.org/draft/2019-09/schema",
        "type": "object",
        "properties": {
            "first_name": {"type": "string"},
            "last_name": {"type": "string"},
            "shipping_address": {"$ref": "/schemas/address"},
            "billing_address": {"$ref": "/schemas/address"},
        },
        "required": ["first_name", "last_name", "shipping_address", "billing_address"],
        "$defs": {
            "address": {
                "$id": "/schemas/address",
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "object",
                "properties": {
                    "street_address": {"type": "string"},
                    "city": {"type": "string"},
                    "state": {"$ref": "#/definitions/state"},
                },
                "required": ["street_address", "city", "state"],
                "definitions": {"state": {"enum": ["CA", "NY", "... etc ..."]}},
            }
        },
    }
    json_store = JsonStore()
    keyword = IdKeyword(json_store)
    document = JsonSchema(json, [keyword])

    # when
    document.load()

    # then
    assert "https://example.com/schemas/address" in json_store
    assert "https://example.com/schemas/customer" in json_store

