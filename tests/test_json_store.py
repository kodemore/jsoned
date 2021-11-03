from jsoned import JsonStore, JsonDocument
import pytest
from os import path


def test_can_instantiate() -> None:
    # given
    instance = JsonStore()

    # then
    assert isinstance(instance, JsonStore)


def test_can_get_default_instance() -> None:
    # given
    instance = JsonStore.default()

    # then
    assert instance == JsonStore.default()


def test_can_fail_on_load_invalid_document() -> None:
    # given
    store = JsonStore.default()

    # then
    with pytest.raises(ValueError):
        store.load(False)


def test_can_load_valid_json_file() -> None:
    # given
    store = JsonStore.default()
    file_name = path.join(path.dirname(__file__), "fixtures", "schema_plain.json")

    # when
    doc = store.load(file_name)

    # then
    assert isinstance(doc, JsonDocument)


def test_fail_on_non_existing_json_file() -> None:
    # given
    store = JsonStore.default()
    file_name = path.join(path.dirname(__file__), "fake", "schema_plain.json")

    # when
    with pytest.raises(FileNotFoundError):
        store.load(file_name)


def test_fail_on_unexpected_file_format() -> None:
    # given
    store = JsonStore.default()
    file_name = path.join(path.dirname(__file__), "test_json_store.py")

    # when
    with pytest.raises(ValueError):
        store.load(file_name)
