from typing import List

from jsoned.errors import ValidationError
from jsoned.validators import Validator
from jsoned.validators.core_validators import Context, ValidatorsIterable

_STACK_VALIDATORS = tuple(["unevaluatedProperties", "unevaluatedItems"])


def validate_all(value, context: Context, validators: ValidatorsIterable) -> bool:
    valid = True
    stacked_validators: List[Validator] = []
    for index, validator in validators.items():
        if index in _STACK_VALIDATORS:
            stacked_validators.append(index)
            continue
        if not validator(value, context):
            valid = False
            break

    if stacked_validators:
        for validator in stacked_validators:
            if not validators[validator](value, context):
                valid = False
                break

    return valid


def validate_any_of(value, context: Context, validators: ValidatorsIterable) -> bool:
    valid = False

    inner_context = context.fork()
    for validator in validators:
        if validator(value, inner_context):
            valid = True

    if not valid:
        error_codes = []
        for error in inner_context.errors:
            error_codes.append(error.code)
        context.errors.append(ValidationError.for_any_of(context.path, set(error_codes)))

    return valid


def validate_one_of(value, context: Context, validators: ValidatorsIterable) -> bool:
    valid = 0
    for validator in validators:
        if validator(value, context.fork()):
            valid += 1

    if valid == 1:
        return True

    context.errors.append(ValidationError.for_one_of(context.path))

    return False


def validate_not(value, context: Context, validator: Validator) -> bool:
    if not validator(value, context):
        return True

    context.errors.append(ValidationError.for_not(context.path))
    return False


def validate_conditionally(
    value,
    context,
    condition_if: Validator = None,
    condition_then: Validator = None,
    condition_else: Validator = None,
):
    if condition_if is None:
        return True

    if condition_if(value, context):
        if condition_then is not None:
            return condition_then(value, context)

        return True

    if condition_else is not None:
        return condition_else(value, context)

    return True
