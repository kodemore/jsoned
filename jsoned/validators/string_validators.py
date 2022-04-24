import re

from jsoned.errors.string_validation_errors import MinimumLengthValidationError, MaximumLengthValidationError, \
    FormatValidationError
from jsoned.string_format import StringFormat
from jsoned.validators import Validator

__all__ = ["StringMinimumLengthValidator", "StringMaximumLengthValidator", "StringFormatValidator", "StringPatternValidator"]

from jsoned.validators.core_validators import Context


class StringMinimumLengthValidator(Validator):
    def __init__(self, expected_minimum: int):
        self.expected_minimum = expected_minimum

    def validate(self, value, context: Context = Context()) -> None:
        if len(value) >= self.expected_minimum:
            return value

        raise MinimumLengthValidationError(expected_minimum=self.expected_minimum, path=context.path)

    def __repr__(self) -> str:
        return f"validate_minimum_length({self.expected_minimum})"


class StringMaximumLengthValidator(Validator):
    def __init__(self, expected_maximum: int):
        self.expected_maximum = expected_maximum

    def validate(self, value, context: Context = Context()) -> None:
        if len(value) <= self.expected_maximum:
            return value

        raise MaximumLengthValidationError(expected_maximum=self.expected_maximum, path=context.path)

    def __repr__(self) -> str:
        return f"validate_maximum_length({self.expected_maximum})"


class StringFormatValidator(Validator):
    def __init__(self, expected_format: str):
        self.expected_format = expected_format

    def validate(self, value, context: Context = Context()) -> None:
        format_validator = StringFormat[self.expected_format]

        if not format_validator(value):
            raise FormatValidationError(path=context.path, expected_format=self.expected_format)

    def __repr__(self) -> str:
        return f"validate_format({self.expected_format})"


class StringPatternValidator(Validator):
    def __init__(self, pattern: str):
        self.pattern = re.compile(pattern)

    def validate(self, value, context: Context = Context()) -> None:
        if not self.pattern.search(value):
            raise FormatValidationError(expected_format=self.pattern.pattern, path=context.path)

    def __repr__(self) -> str:
        return f"validate_pattern({self.pattern})"
