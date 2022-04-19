from jsoned.types import JsonBoolean


def test_can_instantiate() -> None:
    # given
    instance = JsonBoolean(True)

    # then
    assert isinstance(instance, JsonBoolean)


def test_can_compare() -> None:
    assert JsonBoolean(True) == True
    assert JsonBoolean(False) == False

    assert JsonBoolean(True) == JsonBoolean(True)
    assert JsonBoolean(False) == JsonBoolean(False)
    assert JsonBoolean(False) != JsonBoolean(True)
    assert JsonBoolean(True) != False

