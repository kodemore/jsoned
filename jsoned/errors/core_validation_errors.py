from decimal import Decimal
from typing import List, Union

from .validation_error import ValidationError

__all__ = ["EnumValidationError", "TypeValidationError"]


class TypeValidationError(ValidationError):
    code = "type_error"
    expected_types: List[str]
    message = "Passed value must be one of the following type(s) `{expected_types}`."


class EnumValidationError(ValidationError):
    code = "enum_error"
    expected_values: List[Union[str, bool, int, float, Decimal]]
    message = "Passed value must be one of: {expected_values}."
