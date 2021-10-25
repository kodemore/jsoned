from hypothesis import given
from tests.fixtures import json_static_document_fixture
from jsoned import JsonDocument, JsonPointer
from jsoned.types import (
    JsonNull,
    JsonBoolean,
    JsonNumber,
    JsonArray,
    JsonObject,
    JsonString,
    JsonReference,
)


def test_can_instantiate() -> None:
    # when
    doc = JsonDocument(True)

    # then
    assert isinstance(doc, JsonDocument)


def test_json_document_with_null() -> None:
    # when
    doc = JsonDocument(None)

    # then
    assert isinstance(doc, JsonDocument)
    assert isinstance(doc.value, JsonNull)


def test_json_document_with_bool() -> None:
    # when
    doc = JsonDocument(True)

    # then
    assert isinstance(doc, JsonDocument)
    assert isinstance(doc.value, JsonBoolean)

    # when
    doc = JsonDocument(False)

    # then
    assert not doc.value


def test_json_document_with_string() -> None:
    # when
    doc = JsonDocument("Some string")

    # then
    assert isinstance(doc, JsonDocument)
    assert isinstance(doc.value, JsonString)
    assert doc.value == "Some string"


def test_json_document_with_number() -> None:
    # when
    doc = JsonDocument(12.13)

    # then
    assert isinstance(doc, JsonDocument)
    assert isinstance(doc.value, JsonNumber)
    assert doc.value > 12.11
    assert doc.value < 12.14
    assert doc.value == 12.13
    assert doc.value <= 12.13
    assert doc.value >= 12.13
    assert doc.value <= 12.14
    assert doc.value >= 12.12


def test_json_document_with_array() -> None:
    # when
    doc = JsonDocument([1, 2, 3.34, "string", None])

    # then
    assert isinstance(doc, JsonDocument)
    assert isinstance(doc.value, JsonArray)
    assert len(doc.value) == 5


def test_json_document_with_object() -> None:
    # when
    doc = JsonDocument(
        {
            "number": 1.2,
            "array": [True, None],
            "string": "test",
            "bool": False,
            "none": None,
        }
    )

    # then
    assert isinstance(doc, JsonDocument)
    assert isinstance(doc.value, JsonObject)


def test_json_document_with_reference() -> None:
    # when
    doc = JsonDocument({"key": "value", "key_2": {"$ref": "#/key"}})

    # then
    assert isinstance(doc, JsonDocument)


@given(json_static_document_fixture)
def test_can_query_document_with_string_expression(json_data) -> None:
    doc = JsonDocument(json_data)

    # when
    result = doc.query("/schema/items")

    # then
    assert result.value == [{"type": "integer"}, {"type": "string"}]

    # when
    result = doc.query("/schema/items/0")

    # then
    assert result.value == {"type": "integer"}

    # when
    result = doc.query("/schema/items/0/type")

    # then
    result == "integer"


@given(json_static_document_fixture)
def test_can_query_document_with_json_pointer(json_data) -> None:
    # given
    doc = JsonDocument(json_data)

    # when
    result = doc.query(JsonPointer("/schema/items"))

    # then
    assert result.value == [{"type": "integer"}, {"type": "string"}]

    # when
    result = doc.query(JsonPointer("/schema/items/0"))

    # then
    assert result.value == {"type": "integer"}

    # when
    result = doc.query(JsonPointer("/schema/items/0/type"))

    # then
    result == "integer"
