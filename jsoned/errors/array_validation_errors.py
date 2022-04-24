from jsoned.errors.validation_error import ValidationError


class ContainsValidationError(ValidationError):
    code = "contains_error"


class MinimumContainsValidationError(ContainsValidationError):
    expected_minimum: int
    code = "contains_error"
    message = "Array should contain specified value at least `{expected_minimum}` times."


class MaximumContainsValidationError(ContainsValidationError):
    expected_maximum: int
    code = "contains_error"
    message = "Array should contain specified value at most `{expected_maximum}` times."


class MinimumItemsValidationError(ValidationError):
    expected_minimum: int
    code = "minimum_items_error"
    message = "Passed value's length must be greater or equal to set minimum `{expected_minimum}`."


class MaximumItemsValidationError(ValidationError):
    expected_maximum: int
    code = "maximum_items_error"
    message = "Passed value's length must be lower or equal to set maximum `{expected_maximum}`."


class UniqueItemsValidationError(ValidationError):
    code = "unique_items_error"
    message = "Passed value must contain only unique items."
