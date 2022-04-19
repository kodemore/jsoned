from jsoned.types import JsonNull


def test_can_instantiate() -> None:
    # given
    instance = JsonNull()

    # then
    assert isinstance(instance, JsonNull)


def test_can_compare() -> None:
    assert JsonNull() == None

