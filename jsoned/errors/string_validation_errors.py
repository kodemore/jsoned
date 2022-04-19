from abc import ABC

from .validation_error import ValidationError

__all__ = ["FormatValidationError", "LengthValidationError", "MaximumLengthValidationError", "MinimumLengthValidationError"]


class FormatValidationError(ValidationError):
    expected_format: str
    code = "format_error"
    message = "Passed value must conform `{expected_format}` format."


class LengthValidationError(ValidationError, ABC):
    ...


class MinimumLengthValidationError(LengthValidationError):
    code = "min_length_error"
    expected_minimum: int
    message = "Passed value must be at least `{expected_minimum}` characters long."


class MaximumLengthValidationError(LengthValidationError):
    code = "max_length_error"
    expected_maximum: int
    message = "Passed value cannot exceed `{expected_maximum}` characters."
