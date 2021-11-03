from jsoned.keywords import AnchorKeyword, RefKeyword
from jsoned.keywords.ref_keyword import JsonReference
from jsoned import JsonDocument, JsonStore, Uri
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
                }
            }
        }
    }
    doc = JsonDocument(json, [AnchorKeyword()])

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
                "children": {
                    "type": "array",
                    "items": {
                        "$ref": "#/base-object"
                    }
                }
            }
        },
        "strictObject": {
            "additionalProperties": False,
            "$ref": "#/base-object"
        }
    }
    store = JsonStore.default()
    doc_uri = Uri(f"memory://{secrets.token_urlsafe(16)}/document.json")
    json_doc = JsonDocument(json, [RefKeyword(store), AnchorKeyword()])

    # when
    store.add(doc_uri, json_doc)
    parsed_doc = json_doc.value

    # then
    assert isinstance(parsed_doc["genericObject"]["properties"]["children"]["items"], JsonReference)
    assert isinstance(parsed_doc["genericObject"]["properties"]["children"]["items"]["properties"], JsonObject)
    assert "base-object" in json_doc.anchors
    assert parsed_doc["genericObject"] == json_doc.anchors["base-object"]

