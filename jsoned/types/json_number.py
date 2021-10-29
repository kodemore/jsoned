from decimal import Decimal
from typing import Union

from .json_type import JsonType

__all__ = ["JsonNumber"]


class JsonNumber(JsonType):
    type = "number"

    def __init__(self, value: Union[float, int, Decimal], parent: JsonType = None):

        # cast floats to decimal to provide precise numerical operations
        if isinstance(value, float):
            value = Decimal(f"{value}")

        if isinstance(value, (int, Decimal)):
            super().__init__(value, parent)
            return

        raise TypeError(f"Expected int, float or Decimal, got `{type(value)}` instead.")

    def __eq__(self, other):
        if isinstance(other, JsonType):
            return self._value == other._value
        elif isinstance(other, float):
            return self._value == Decimal(f"{other}")
        else:
            return self._value == other

    def __lt__(self, other):
        if isinstance(other, JsonType):
            return self._value < other._value
        elif isinstance(other, float):
            return self._value < Decimal(f"{other}")
        else:
            return self._value < other

    def __le__(self, other):
        if isinstance(other, JsonType):
            return self._value <= other._value
        elif isinstance(other, float):
            return self._value <= Decimal(f"{other}")
        else:
            return self._value <= other

    def __gt__(self, other):
        if isinstance(other, JsonType):
            return self._value > other._value
        elif isinstance(other, float):
            return self._value > Decimal(f"{other}")
        else:
            return self._value > other

    def __ge__(self, other):
        if isinstance(other, JsonType):
            return self._value >= other._value
        elif isinstance(other, float):
            return self._value >= Decimal(f"{other}")
        else:
            return self._value >= other
