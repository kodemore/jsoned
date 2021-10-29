from jsoned import JsonDocument
from jsoned.keywords import RefKeyword
from jsoned.keywords.ref_keyword import JsonReference
from os import path


def test_can_resolve_local_ref() -> None:
    for i in range(1, 10000):
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


def test_can_resolve_local_recursive_ref() -> None:
    # given
    json_data = {
        "node": {
            "id": "string",
            "name": "string",
            "children": [{
                "$ref": "#",
            }],
        },
    }

    doc = JsonDocument(json_data)

    # when
    value = doc.value

    # then
    assert value["node"]["children"][0] == value

