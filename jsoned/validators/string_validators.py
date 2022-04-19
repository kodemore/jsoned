import re

from jsoned.errors.string_validation_errors import MinimumLengthValidationError, MaximumLengthValidationError, \
    FormatValidationError
from jsoned.string_format import StringFormat
from jsoned.validators import Validator

__all__ = ["StringMinimumLengthValidator", "StringMaximumLengthValidator", "StringFormatValidator", "StringPatternValidator"]


class StringMinimumLengthValidator(Validator):
    def __init__(self, expected_minimum: int, key: str = "@minimum-length", parent: Validator = None):
        self.expected_minimum = expected_minimum
        super().__init__(key, parent)

    def validate(self, value) -> None:
        if len(value) >= self.expected_minimum:
            return value

        raise MinimumLengthValidationError(expected_minimum=self.expected_minimum)

    def __repr__(self) -> str:
        return f"validate_minimum_length({self.expected_minimum})"


class StringMaximumLengthValidator(Validator):
    def __init__(self, expected_maximum: int, key: str = "@maximum-length", parent: Validator = None):
        self.expected_maximum = expected_maximum
        super().__init__(key, parent)

    def validate(self, value) -> None:
        if len(value) <= self.expected_maximum:
            return value

        raise MaximumLengthValidationError(expected_maximum=self.expected_maximum)

    def __repr__(self) -> str:
        return f"validate_maximum_length({self.expected_maximum})"


class StringFormatValidator(Validator):
    def __init__(self, expected_format: str, key: str = "@format", parent: Validator = None):
        self.expected_format = expected_format
        super().__init__(key, parent)

    def validate(self, value) -> None:
        format_validator = StringFormat[self.expected_format]

        if not format_validator(value):
            raise FormatValidationError(path=self.path, expected_format=self.expected_format)

    def __repr__(self) -> str:
        return f"validate_format({self.expected_format})"


class StringPatternValidator(Validator):
    def __init__(self, pattern: str, key: str = "@pattern", parent: Validator = None):
        self.pattern = pattern
        super().__init__(key, parent)

    def validate(self, value) -> None:
        if not re.search(self.pattern, value):
            raise FormatValidationError(expected_format=self.pattern, path=self.path)

    def __repr__(self) -> str:
        return f"validate_pattern({self.pattern})"
