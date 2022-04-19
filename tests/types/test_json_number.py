from typing import Any

import pytest
from decimal import Decimal
from jsoned.types import JsonNumber


def test_can_instantiate() -> None:
    # given
    instance = JsonNumber(1)

    # then
    assert isinstance(instance, JsonNumber)


def test_can_init_from_float() -> None:
    # given
    instance = JsonNumber(12.12)

    # then
    assert isinstance(instance, JsonNumber)
    instance == 12.12


def test_can_init_from_int() -> None:
    # given
    instance = JsonNumber(10)

    # then
    assert isinstance(instance, JsonNumber)
    instance == 10


def test_can_do_comparison() -> None:
    # given
    instance = JsonNumber(10)

    # then
    assert instance <= JsonNumber(10)
    assert instance < 11
    assert instance < JsonNumber(11)
    assert instance > 9
    assert instance > JsonNumber(9)
    assert instance >= JsonNumber(9)
    assert instance == 10
    assert instance == JsonNumber(10)


@pytest.mark.parametrize("a,b,expected", [
    [1, 1, JsonNumber(2)],
    [1, 1.2, JsonNumber(2.2)],
    [1, Decimal("1.2"), JsonNumber(2.2)],
    [1.2, Decimal("1.2"), JsonNumber(2.4)],
    [1.2, JsonNumber(1), JsonNumber(2.2)],
])
def test_can_do_addition(a: JsonNumber, b: Any, expected: JsonNumber) -> None:
    # given
    instance = JsonNumber(a)

    # when
    result = instance + b

    # then
    assert result == expected
    assert isinstance(result, JsonNumber)
