import itertools
from collections.abc import Iterable
from typing import Union, Any, Sequence, Mapping

from jsoned.errors import ValidationError
from jsoned.validators.core_validators import Context, Validator, ValidatorsCollection


def validate_array_items(value: Iterable, context: Context, items_validator: Validator) -> bool:
    if not isinstance(value, list):  # ignore non-list items
        return True

    if "evaluated_items" not in context:
        context["evaluated_items"] = set()

    valid = True
    for index, item in enumerate(value):
        if not items_validator(item, context + str(index)):
            valid = False
        else:
            context["evaluated_items"].add((context + str(index)).path)

    return valid


def validate_array_prefixed_items(value: Iterable, context: Context, items_validator: ValidatorsCollection, additional_items: Union[bool, Validator] = None) -> bool:
    if not isinstance(value, list):  # ignore non-list items
        return True

    valid = True
    if "evaluated_items" not in context:
        context["evaluated_items"] = set()

    for index, item in enumerate(value):
        if index < len(items_validator):
            validator = items_validator[index]

            if not validator(item, context + str(index)):
                valid = False
            else:
                context["evaluated_items"].add((context + str(index)).path)

        elif isinstance(additional_items, bool):
            if additional_items is True:
                context["evaluated_items"].add((context + str(index)).path)
                continue
            if additional_items is False:
                valid = False
                context.errors.append(ValidationError.for_array_additional_items(context.path, index=index))
                break
        elif additional_items is None:
            break
        else:
            if not additional_items(item, Context()):
                valid = False
                break
            context["evaluated_items"].add((context + str(index)).path)

    return valid


def validate_array_contains(
    value: Iterable,
    context: Context,
    item_validator: Validator,
    minimum_contains: int = 1,
    maximum_contains: int = 0
) -> bool:
    if not isinstance(value, list):
        return True

    if "evaluated_items" not in context:
        context["evaluated_items"] = set()

    contains_count = 0
    valid = True

    for index, item in enumerate(value):
        item_path = (context + str(index)).path
        if item_validator(item, Context()):
            contains_count += 1
            context["evaluated_items"].add(item_path)

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

    if contains_count < minimum_contains:
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
    if not isinstance(value, list):  # ignore non-arrays
        return True

    value_length = len(value)

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


def validate_array_unevaluated_items(
    value: Iterable,
    context: Context,
    item_validator: Validator = None
) -> bool:
    if not isinstance(value, list):  # ignore non-arrays
        return True
    if "evaluated_items" not in context:
        context["evaluated_items"] = set()

    for index, item in enumerate(value):
        evaluated_item = (context + str(index)).path
        if evaluated_item in context["evaluated_items"]:
            continue

        if item_validator is None:
            context.errors.append(
                ValidationError.for_array_unevaluated_items(context.path, index=index)
            )
            return False
        else:
            if not item_validator(item, Context()):
                context.errors.append(
                    ValidationError.for_array_unevaluated_items(context.path, index=index)
                )
                return False

    return True


def _swap_bool(value: Any, true: Any = object(), false: Any = object()) -> Any:
    if value is True:
        return true
    elif value is False:
        return false
    return value


def _equal_sequence(a: Sequence, b: Sequence) -> bool:
    if len(a) != len(b):
        return False
    return all(_equal(i, j) for i, j in zip(a, b))


def _equal_mapping(a: Mapping, b: Mapping) -> bool:
    if len(a) != len(b):
        return False
    return all(
        key in b and _equal(value, b[key])
        for key, value in a.items()
    )


def _equal(a: Any, b: Any) -> bool:
    if isinstance(a, str) or isinstance(b, str):
        return a == b
    if isinstance(a, Sequence) and isinstance(b, Sequence):
        return _equal_sequence(a, b)
    if isinstance(a, Mapping) and isinstance(b, Mapping):
        return _equal_mapping(a, b)
    return _swap_bool(a) == _swap_bool(b)


def validate_array_unique(value: Iterable, context: Context) -> bool:
    if not isinstance(value, list):
        return True

    try:
        index = 0
        sort = sorted(_swap_bool(i) for i in value)
        sliced = itertools.islice(sort, 1, None)

        for i, j in zip(sort, sliced):
            if _equal(i, j):
                context.errors.append(
                    ValidationError.for_array_non_unique(context.path + str(index))
                )
                return False
            index += 1
    except (NotImplementedError, TypeError):
        seen = []
        index = 0
        for element in value:
            element = _swap_bool(element)

            for i in seen:
                if _equal(i, element):
                    context.errors.append(
                        ValidationError.for_array_non_unique(context.path + str(index))
                    )
                    return False
            index += 1
            seen.append(element)

    return True
