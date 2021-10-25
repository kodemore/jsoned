from decimal import Decimal
from typing import TypeVar, List, Dict

__all__ = ["NoneType", "AnyJsonType"]

NoneType = type(None)
AnyJsonType = TypeVar(
    "AnyJsonType", NoneType, bool, int, float, Decimal, str, List, Dict
)
