from decimal import Decimal

import pytest

from jsoned import Uri
from jsoned.types import JsonObject, JsonString, JsonNumber, JsonNull


def test_can_instantiate() -> None:
    # given
    instance = JsonObject({"a": 1})

    # then
    assert isinstance(instance, JsonObject)


def test_can_successfully_parse() -> None:
    doc = JsonObject({"integer": 1, "float": 1.2, "decimal": Decimal("1.3"), "nested": {"a": 1}, "null": None})
    assert isinstance(doc, JsonObject)
    assert isinstance(doc["integer"], JsonNumber)
    assert isinstance(doc["float"], JsonNumber)
    assert isinstance(doc["decimal"], JsonNumber)
    assert isinstance(doc["nested"], JsonObject)
    assert isinstance(doc["null"], JsonNull)


def test_can_compare() -> None:
    assert JsonObject({"a": 1}) == JsonObject({"a": 1})
    assert JsonObject({"a": 1}) != JsonObject({"a": 2})


def test_can_get_item() -> None:
    # given
    instance = JsonObject({"a": 1})

    # when
    a = instance["a"]

    # then
    assert a == 1


def test_can_set_item() -> None:
    # given
    instance = JsonObject({"a": 1})

    # when
    instance["a"] = "a"

    # then
    assert instance["a"] == "a"
    assert isinstance(instance["a"], JsonString)
    assert instance["a"].parent == instance


def test_cannot_set_invalid_item() -> None:
    # given
    instance = JsonObject({"a": 1})

    # then
    with pytest.raises(ValueError):
        instance["a"] = Uri("a")


def test_can_retrieve_keys() -> None:
    # given
    instance = JsonObject({"a": 1, "b": 2})

    # when
    keys = instance.keys()

    # then
    assert len(keys) == 2
    assert "a" in keys
    assert "b" in keys
