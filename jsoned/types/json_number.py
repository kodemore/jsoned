from __future__ import annotations
from decimal import Decimal
from typing import Union, overload

from .json_type import JsonType

__all__ = ["JsonNumber"]


class JsonNumber(JsonType):
    type = JsonType.NUMBER

    def __init__(self, value: Union[float, int, Decimal], parent: JsonType = None, key: str = ""):
        # cast floats to decimal to provide precise numerical operations
        if isinstance(value, (int, float)):
            value = Decimal(f"{value}")

        if isinstance(value, Decimal):
            super().__init__(value, parent, key)
            return

        raise TypeError(f"Expected int, float or Decimal representation, got `{type(value)}` instead.")

    @overload
    def __eq__(self, other: "JsonNumber") -> bool:
        ...

    @overload
    def __eq__(self, other: float) -> bool:
        ...

    @overload
    def __eq__(self, other: int) -> bool:
        ...

    @overload
    def __eq__(self, other: Decimal) -> bool:
        ...

    def __eq__(self, other):
        if isinstance(other, JsonNumber):
            return self._value == other._value
        elif isinstance(other, float):
            return self._value == Decimal(f"{other}")
        elif isinstance(other, (Decimal, int)):
            return self._value == other

        raise TypeError(f"Expected numerical type or JsonNumber, got `{type(other)}` instead.")

    @overload
    def __lt__(self, other: "JsonNumber") -> bool:
        ...

    @overload
    def __lt__(self, other: float) -> bool:
        ...

    @overload
    def __lt__(self, other: int) -> bool:
        ...

    @overload
    def __lt__(self, other: Decimal) -> bool:
        ...

    def __lt__(self, other):
        if isinstance(other, JsonNumber):
            return self._value < other._value
        elif isinstance(other, float):
            return self._value < Decimal(f"{other}")
        elif isinstance(other, (Decimal, int)):
            return self._value < other

        raise TypeError(f"Expected numerical type or JsonNumber, got `{type(other)}` instead.")

    @overload
    def __le__(self, other: "JsonNumber") -> bool:
        ...

    @overload
    def __le__(self, other: float) -> bool:
        ...

    @overload
    def __le__(self, other: int) -> bool:
        ...

    @overload
    def __le__(self, other: Decimal) -> bool:
        ...

    def __le__(self, other):
        if isinstance(other, JsonNumber):
            return self._value <= other._value
        elif isinstance(other, float):
            return self._value <= Decimal(f"{other}")
        elif isinstance(other, (Decimal, int)):
            return self._value <= other

        raise TypeError(f"Expected numerical type or JsonNumber, got `{type(other)}` instead.")

    @overload
    def __gt__(self, other: "JsonNumber") -> bool:
        ...

    @overload
    def __gt__(self, other: float) -> bool:
        ...

    @overload
    def __gt__(self, other: int) -> bool:
        ...

    @overload
    def __gt__(self, other: Decimal) -> bool:
        ...

    def __gt__(self, other):
        if isinstance(other, JsonNumber):
            return self._value > other._value
        elif isinstance(other, float):
            return self._value > Decimal(f"{other}")
        elif isinstance(other, (Decimal, int)):
            return self._value > other

        raise TypeError(f"Expected numerical type or JsonNumber, got `{type(other)}` instead.")

    @overload
    def __ge__(self, other: "JsonNumber") -> bool:
        ...

    @overload
    def __ge__(self, other: float) -> bool:
        ...

    @overload
    def __ge__(self, other: int) -> bool:
        ...

    @overload
    def __ge__(self, other: Decimal) -> bool:
        ...

    def __ge__(self, other):
        if isinstance(other, JsonNumber):
            return self._value >= other._value
        elif isinstance(other, float):
            return self._value >= Decimal(f"{other}")
        elif isinstance(other, (Decimal, int)):
            return self._value >= other

        raise TypeError(f"Expected numerical type or JsonNumber, got `{type(other)}` instead.")

    @overload
    def __add__(self, other: int) -> JsonNumber:
        ...

    @overload
    def __add__(self, other: float) -> JsonNumber:
        ...

    @overload
    def __add__(self, other: Decimal) -> JsonNumber:
        ...

    @overload
    def __add__(self, other: JsonNumber) -> JsonNumber:
        ...

    def __add__(self, other) -> JsonNumber:
        if isinstance(other, JsonNumber):
            result = self._value + other._value
            return JsonNumber(result)
        elif isinstance(other, float):
            result = self._value + Decimal(f"{other}")
            return JsonNumber(result)
        elif isinstance(other, int):
            result = self._value + other
            return JsonNumber(result)
        elif isinstance(other, Decimal):
            result = other + self._value
            return JsonNumber(result)

        raise TypeError(f"Expected numerical type or JsonNumber, got `{type(other)}` instead.")

    def __int__(self) -> int:
        return int(self._value)

    def __float__(self) -> float:
        return float(self._value)
