from decimal import Decimal
from typing import Union

from jsoned.errors.number_validation_error import MultipleOfValidationError, MinimumValidationError, \
    MaximumValidationError
from jsoned.validators import Validator

__all__ = ["NumberMultipleOfValidator", "NumberMaximumValidator", "NumberMinimumValidator"]

NumberUnion = Union[int, float, Decimal]


class NumberMultipleOfValidator(Validator):
    def __init__(self, multiple_of: Decimal, key: str = "@multiple-of", parent: Validator = None):
        self.multiple_of = multiple_of
        super().__init__(key, parent)

    def validate(self, value) -> None:
        if not isinstance(value, Decimal):
            value = Decimal(str(value))

        if value % self.multiple_of != 0:  # type: ignore
            raise MultipleOfValidationError(multiple_of=self.multiple_of, path=self.path)

    def __repr__(self) -> str:
        return f"validate_multiple_of({self.multiple_of})"


class NumberMinimumValidator(Validator):
    def __init__(self, expected_minimum: Decimal, exclusive: bool = False, key: str = "@minimum", parent: Validator = None):
        self.expected_minimum = expected_minimum
        self.exclusive = exclusive
        super().__init__(key, parent)

    def validate(self, value: NumberUnion):
        if self.exclusive and value <= self.expected_minimum:
            raise MinimumValidationError(expected_minimum=self.expected_minimum, path=self.path)

        if not self.exclusive and value < self.expected_minimum:
            raise MinimumValidationError(expected_minimum=self.expected_minimum, path=self.path)

    def __repr__(self) -> str:
        return f"validate_minimum({self.expected_minimum})"


class NumberMaximumValidator(Validator):
    def __init__(self, expected_maximum: Decimal, exclusive: bool = False, key: str = "@maximum", parent: Validator = None):
        self.expected_maximum = expected_maximum
        self.exclusive = exclusive
        super().__init__(key, parent)

    def validate(self, value: NumberUnion):
        if self.exclusive and value >= self.expected_maximum:
            raise MaximumValidationError(expected_maximum=self.expected_maximum, path=self.path)

        if not self.exclusive and value > self.expected_maximum:
            raise MaximumValidationError(expected_maximum=self.expected_maximum, path=self.path)

    def __repr__(self) -> str:
        return f"validate_maximum({self.expected_maximum})"
