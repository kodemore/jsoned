import re
from functools import partial
from typing import Pattern

from jsoned.errors.validation_error import ValidationError
from jsoned.string_format import StringFormat
from jsoned.validators.composition_validators import validate_all
from jsoned.validators.core_validators import Context, ValidatorsMap, Validator


def create_string_validator(
    expected_minimum_length: int = -1,
    expected_maximum_length: int = -1,
    expected_pattern: Pattern = None,
    expected_format: str = None
) -> Validator:
    validators = ValidatorsMap()
    if expected_minimum_length > -1 or expected_maximum_length > -1:
        validators["string_length"] = partial(
            validate_string_length,
            expected_maximum=expected_maximum_length,
            expected_minimum=expected_minimum_length
        )

    if expected_pattern is not None:
        validators["string_pattern"] = partial(
            validate_string_pattern,
            expected_pattern=expected_pattern
        )

    if expected_format is not None:
        validators["string_format"] = partial(
            validate_string_format,
            expected_format=expected_format,
        )

    def _validate_string(value, context: Context) -> bool:
        return validate_all(value, context, validators)

    return _validate_string


def validate_string(
    value,
    context: Context = None,
    expected_minimum_length: int = -1,
    expected_maximum_length: int = -1,
    expected_pattern: Pattern = None,
    expected_format: str = None,
) -> bool:
    context = context or Context()
    return create_string_validator(
        expected_minimum_length,
        expected_maximum_length,
        expected_pattern,
        expected_format
    )(value, context)


def validate_string_length(
    value,
    context: Context,
    expected_minimum: int = 0,
    expected_maximum: int = 0,
) -> bool:
    if not isinstance(value, str):
        return True

    current_length = len(value)

    if expected_minimum >= 0 and current_length < expected_minimum:
        context.errors.append(
            ValidationError.for_string_minimum_length(path=context.path, expected_minimum=expected_minimum)
        )
        return False

    if 0 < expected_maximum < current_length:
        context.errors.append(
            ValidationError.for_string_maximum_length(path=context.path, expected_maximum=expected_maximum)
        )
        return False

    return True


def validate_string_format(value, context: Context, expected_format: str) -> bool:
    if not isinstance(value, str):
        return True
    format_validator = StringFormat[expected_format]
    if not format_validator(value):
        context.errors.append(
            ValidationError.for_string_format(path=context.path, expected_format=expected_format)
        )
        return False

    return True


def validate_string_pattern(value, context: Context, expected_pattern: str) -> bool:
    if not isinstance(value, str):
        return True
    pattern = re.compile(expected_pattern)
    if not pattern.search(value):
        context.errors.append(
            ValidationError.for_string_pattern(path=context.path, expected_pattern=expected_pattern)
        )
        return False

    return True
