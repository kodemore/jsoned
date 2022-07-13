from typing import Iterable, Sized, Union

from jsoned.errors import ValidationError
from jsoned.validators.core_validators import Context, Validator, ValidatorsCollection


def validate_array_items(value: Iterable, context: Context, items_validator: Validator) -> bool:
    valid = True
    for index, item in enumerate(value):
        if not items_validator(item, context + str(index)):
            valid = False

    return valid


def validate_array_prefixed_items(value: Iterable, context: Context, items_validator: ValidatorsCollection, additional_items: Union[bool, Validator] = True) -> bool:
    i = -1
    valid = True
    additional_items = additional_items or False

    for item in value:
        i += 1
        if i < len(items_validator):
            validator = items_validator[i]
            if not validator(item, context + str(i)):
                valid = False
        elif isinstance(additional_items, bool):
            if additional_items is True:
                break
            if additional_items is False:
                valid = False
                context.errors.append(ValidationError.for_array_additional_items(context.path, index=i))
                break
        elif not additional_items(item):
            valid = False
            break

    return valid


def validate_array_contains(
    value: Iterable,
    context: Context,
    item_validator: Validator,
    minimum_contains: int = 0,
    maximum_contains: int = 0
) -> bool:
    contains_count = 0
    valid = True

    for item in value:
        if item_validator(item, Context()):
            contains_count += 1

    if minimum_contains and contains_count < minimum_contains:
        valid = False
        context.errors.append(
            ValidationError.for_array_minimum_contains(context.path, expected_minimum=minimum_contains)
        )

    if maximum_contains and contains_count > maximum_contains:
        valid = False
        context.errors.append(
            ValidationError.for_array_maximum_contains(context.path, expected_maximum=maximum_contains)
        )

    if not minimum_contains and contains_count < 1:
        context.errors.append(
            ValidationError.for_array_minimum_contains(context.path, expected_minimum=1)
        )
        valid = False

    return valid


def validate_array_length(
    value: Iterable,
    context: Context,
    expected_minimum: int = 0,
    expected_maximum: int = 0,
) -> bool:
    valid = True
    if isinstance(value, Sized):
        value_length = len(value)
    else:
        value_length = len([1 for _ in value])

    if expected_minimum and value_length < expected_minimum:
        valid = False
        context.errors.append(
            ValidationError.for_array_minimum_length(context.path, expected_minimum=expected_minimum)
        )

    if expected_maximum and value_length > expected_maximum:
        valid = False
        context.errors.append(
            ValidationError.for_array_maximum_length(context.path, expected_maximum=expected_maximum)
        )

    return valid


def validate_array_unique(value: Iterable, context: Context) -> bool:
    valid = True
    seen = set()
    i = 0
    for item in value:
        if item not in seen:
            seen.add(item)
        else:
            valid = False
            context.errors.append(
                ValidationError.for_array_non_unique(context.path + str(i))
            )
            break
        i += 1

    return valid
