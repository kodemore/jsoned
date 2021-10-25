from jsoned import JsonDocument
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

    doc = JsonDocument(json_data)

    # when
    value = doc.value

    # then
    assert isinstance(value["properties"]["name"], JsonReference)
    assert value["properties"]["name"] == {"type": "string"}
