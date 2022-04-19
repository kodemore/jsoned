from jsoned.types import JsonString
from collections import UserString


def test_can_instantiate() -> None:
    # given
    instance = JsonString("test")

    # then
    assert isinstance(instance, JsonString)
    assert isinstance(instance, UserString)


def test_can_compare() -> None:
    assert JsonString("test") == "test"
    assert JsonString("123") != "test"


def test_can_add() -> None:
    result = JsonString("abc") + "def"

    assert isinstance(result, JsonString)
