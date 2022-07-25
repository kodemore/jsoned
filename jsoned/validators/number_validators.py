from __future__ import annotations

from decimal import Decimal
from functools import partial

from jsoned.errors import ValidationError
from jsoned.validators.composition_validators import validate_all
from jsoned.validators.core_validators import Context, ValidatorsMap, Validator


def validate_minimum(value, context: Context, expected_minimum: Decimal, exclusive: bool = False) -> bool:
    if not isinstance(value, Decimal):
        try:
            value = Decimal(str(value))
        except Exception:  # Ignore non-numeric types
            return True

    if exclusive:
        return validate_exclusive_minimum(value, context, expected_minimum)

    if value < expected_minimum:
        context.errors.append(
            ValidationError.for_number_minimum(path=context.path, expected_minimum=expected_minimum)
        )
        return False

    return True


def validate_exclusive_minimum(value, context: Context, expected_minimum: Decimal) -> bool:
    if not isinstance(value, Decimal):
        try:
            value = Decimal(str(value))
        except Exception:  # Ignore non-numeric types
            return True

    if value <= expected_minimum:
        context.errors.append(
            ValidationError.for_number_exclusive_minimum(path=context.path, expected_minimum=expected_minimum)
        )
        return False

    return True


def validate_maximum(value, context: Context, expected_maximum: Decimal, exclusive: bool = False) -> bool:
    if not isinstance(value, Decimal):
        try:
            value = Decimal(str(value))
        except Exception:  # Ignore non-numeric types
            return True

    if exclusive:
        return validate_exclusive_maximum(value, context, expected_maximum)

    if value > expected_maximum:
        context.errors.append(
            ValidationError.for_number_maximum(path=context.path, expected_maximum=expected_maximum)
        )
        return False

    return True


def validate_exclusive_maximum(value, context: Context, expected_maximum: Decimal) -> bool:
    if not isinstance(value, Decimal):
        try:
            value = Decimal(str(value))
        except Exception:  # Ignore non-numeric types
            return True

    if value >= expected_maximum:
        context.errors.append(
            ValidationError.for_number_exclusive_maximum(path=context.path, expected_maximum=expected_maximum)
        )
        return False

    return True


def validate_multiple_of(value, context: Context, multiple_of: Decimal) -> bool:
    if not isinstance(value, Decimal):
        try:
            value = Decimal(str(value))
        except Exception:  # Ignore non-numeric types
            return True

    try:
        if value % multiple_of != 0:  # type: ignore
            context.errors.append(
                ValidationError.for_number_multiple_of(path=context.path, multiple_of=multiple_of)
            )
            return False
    except Exception:
        return False

    return True


def create_number_validator(
    expected_minimum: Decimal = None,
    expected_maximum: Decimal = None,
    exclusive_comparison: bool = False,
    multiple_of: Decimal = None,
) -> Validator:

    validators = ValidatorsMap()
    if expected_maximum is not None:
        if exclusive_comparison:
            validators["maximum"] = partial(validate_exclusive_maximum, expected_maximum=expected_maximum)
        else:
            validators["maximum"] = partial(validate_maximum, expected_maximum=expected_maximum)

    if expected_minimum is not None:
        if exclusive_comparison:
            validators["minimum"] = partial(validate_exclusive_minimum, expected_minimum=expected_minimum)
        else:
            validators["minimum"] = partial(validate_minimum, expected_minimum=expected_minimum)

    if multiple_of is not None:
        validators["multiple_of"] = partial(validate_multiple_of, multiple_of=multiple_of)

    def _validate_number(value, context: Context) -> bool:
        if not isinstance(value, Decimal):
            value = Decimal(str(value))
        return validate_all(value, context, validators)

    return _validate_number


def validate_number(
    value,
    context: Context = None,
    expected_minimum: Decimal = None,
    expected_maximum: Decimal = None,
    exclusive_comparison: bool = False,
    multiple_of: Decimal = None,
) -> bool:
    context = context or Context()
    return create_number_validator(
        expected_minimum,
        expected_maximum,
        exclusive_comparison,
        multiple_of,
    )(value, context)
