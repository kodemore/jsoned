from jsoned.keywords import AnchorKeyword, RefKeyword
from jsoned.keywords.ref_keyword import JsonReference
from jsoned import JsonSchema, JsonStore, Uri
from jsoned.types import JsonObject
import secrets


def test_can_instantiate() -> None:
    # given
    keyword = AnchorKeyword()

    # then
    assert isinstance(keyword, AnchorKeyword)


def test_can_define_anchor() -> None:
    # given
    json = {
        "type": "object",
        "properties": {
            "$anchor": "props",
            "children": {
                "type": "array",
                "items": {
                    "type": "object",
                },
            },
        },
    }
    doc = JsonSchema(json, [AnchorKeyword()])

    # when
    result = doc.query("/props")

    # then
    assert "props" in doc.anchors
    assert isinstance(result, JsonObject)
    assert "children" in result


def test_can_reference_defined_anchor() -> None:
    # given
    json = {
        "genericObject": {
            "$anchor": "base-object",
            "type": "object",
            "properties": {
                "children": {"type": "array", "items": {"$ref": "#/base-object"}}
            },
        },
        "strictObject": {"additionalProperties": False, "$ref": "#/base-object"},
    }
    store = JsonStore.default()
    schema = JsonSchema(json, [RefKeyword(store), AnchorKeyword()])

    # when
    generic_ref = schema.query("/genericObject/properties/children/items")

    # then
    assert isinstance(
        generic_ref, JsonReference
    )
    assert isinstance(
        generic_ref["properties"],
        JsonObject,
    )
    assert "base-object" in schema.anchors
    assert schema.query("/genericObject") == schema.anchors["base-object"]
