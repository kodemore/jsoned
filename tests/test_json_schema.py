from hypothesis import given

from jsoned import JsonSchema, JsonPointer
from jsoned.types import (
    JsonObject, JsonArray,
)
from tests.fixtures import json_static_document_fixture


def test_can_instantiate() -> None:
    # when
    doc = JsonSchema({})

    # then
    assert isinstance(doc, JsonSchema)


def test_can_create_from_dict() -> None:
    # when
    doc = JsonSchema(
        {
            "number": 1.2,
            "array": [True, None],
            "string": "test",
            "bool": False,
            "none": None,
        }
    )

    # then
    assert isinstance(doc, JsonSchema)
    assert isinstance(doc.value, JsonObject)


def test_can_create_from_list() -> None:
    # when
    doc = JsonSchema(
        [{
            "number": 1.2,
            "array": [True, None],
            "string": "test",
            "bool": False,
            "none": None,
        }]
    )

    # then
    assert isinstance(doc, JsonSchema)
    assert isinstance(doc.value, JsonArray)


def test_json_document_with_reference() -> None:
    # when
    doc = JsonSchema({"key": "value", "key_2": {"$ref": "#/key"}})

    # then
    assert isinstance(doc, JsonSchema)


@given(json_static_document_fixture)
def test_can_query_document_with_string_expression(json_data) -> None:
    doc = JsonSchema(json_data)

    # when
    result = doc.query("/schema/items")

    # then
    assert result._value == [{"type": "integer"}, {"type": "string"}]

    # when
    result = doc.query("/schema/items/0")

    # then
    assert result._value == {"type": "integer"}

    # when
    result = doc.query("/schema/items/0/type")

    # then
    result == "integer"
    result.path == "/schema/items/0/type"

    # when
    result = doc.query("/")

    # then
    result.path == "/"


@given(json_static_document_fixture)
def test_can_query_document_with_json_pointer(json_data) -> None:
    # given
    doc = JsonSchema(json_data)

    # when
    result = doc.query(JsonPointer("/schema/items"))

    # then
    assert result._value == [{"type": "integer"}, {"type": "string"}]

    # when
    result = doc.query(JsonPointer("/schema/items/0"))

    # then
    assert result._value == {"type": "integer"}

    # when
    result = doc.query(JsonPointer("/schema/items/0/type"))

    # then
    result == "integer"
