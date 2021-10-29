from jsoned import JsonStore
import pytest


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
