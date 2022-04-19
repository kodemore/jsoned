from decimal import Decimal

from .validation_error import ValidationError


class MultipleOfValidationError(ValidationError):
    multiple_of: Decimal
    code = "multiple_of_error"
    message = "Passed value must be multiple of `{multiple_of}`."


class ComparisonValidationError(ValidationError):
    code = "comparison_error"
    message = "Passed value is invalid."


class EqualityValidationError(ComparisonValidationError):
    code = "equal_error"
    message = "Passed value {passed_value} does not equal {expected_value}."


class RangeValidationError(ComparisonValidationError):
    pass


class MinimumValidationError(RangeValidationError):
    expected_minimum: Decimal
    code = "minimum_error"
    message = "Passed value must be greater or equal to set minimum `{expected_minimum}`."


class MaximumValidationError(RangeValidationError):
    expected_maximum: Decimal
    code = "maximum_error"
    message = "Passed value must be lower or equal to set maximum `{expected_maximum}`."
