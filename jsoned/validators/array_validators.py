from typing import List

from jsoned.errors import ValidationError, MinimumContainsValidationError, MaximumContainsValidationError
from jsoned.errors.array_validation_errors import MinimumItemsValidationError, MaximumItemsValidationError, \
    UniqueItemsValidationError
from jsoned.errors.core_validation_errors import TypeValidationError
from jsoned.types import JsonType
from jsoned.validators.core_validators import CompoundValidator, Context, Validator


class ArrayValidator(CompoundValidator):
    items: CompoundValidator = None
    prefix_items: List[CompoundValidator] = None

    def validate(self, value, context: Context = Context()):
        if not isinstance(value, list):
            raise TypeValidationError(expected_types=[str(JsonType.ARRAY)])

        index = 0
        if self.prefix_items:
            while index < len(self.prefix_items):
                if index >= len(value):
                    self.prefix_items[index].validate(None, context + str(index))
                    continue

                self.prefix_items[index].validate(value[index], context + str(index))
                index += 1

        if self.items is None:
            return

        while index < len(value):
            self.items.validate(value[index], context + str(index))
            index += 1


class ArrayContainsValidator(Validator):
    minimum_contains: int = 1
    maximum_contains: int = None

    def __init__(self, checker: Validator):
        self.item_validator = checker

    def validate(self, value, context: Context = Context()) -> None:
        valid = 0
        for item in value:
            try:
                self.item_validator.validate(item)
                valid += 1
            except ValidationError:
                continue

        if valid < self.minimum_contains:
            raise MinimumContainsValidationError(expected_minimum=self.minimum_contains, path=context.path)

        if self.maximum_contains and valid > self.maximum_contains:
            raise MaximumContainsValidationError(expected_maximum=self.maximum_contains, path=context.path)


class ArrayMinimumLengthValidator(Validator):
    def __init__(self, expected_minimum: int):
        self.expected_minimum = expected_minimum

    def validate(self, value, context: Context = Context()) -> None:
        if len(value) >= self.expected_minimum:
            return value

        raise MinimumItemsValidationError(expected_minimum=self.expected_minimum, path=context.path)

    def __repr__(self) -> str:
        return f"validate_minimum_items({self.expected_minimum})"


class ArrayMaximumLengthValidator(Validator):
    def __init__(self, expected_maximum: int):
        self.expected_maximum = expected_maximum

    def validate(self, value, context: Context = Context()) -> None:
        if len(value) <= self.expected_maximum:
            return value

        raise MaximumItemsValidationError(expected_maximum=self.expected_maximum, path=context.path)

    def __repr__(self) -> str:
        return f"validate_maximum_items({self.expected_maximum})"


class ArrayUniqueValidators(Validator):
    def validate(self, value, context: Context = Context()) -> None:
        seen = set()
        for key, item in enumerate(value):
            if item in seen:
                raise UniqueItemsValidationError(path=context.path + str(key))
            seen.add(item)

