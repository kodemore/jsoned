import dataclasses
import re
from functools import partial
from typing import List, Pattern, Dict, Callable

from jsoned.errors.object_validation_errors import RequiredPropertyValidationError, MinimumPropertiesValidationError, \
    MaximumPropertiesValidationError, DependentValidationError
from jsoned.validators.core_validators import Validator, Context, CompoundValidator


class RequiredPropertiesValidator(Validator):
    def __init__(self, required_properties: List[str]):
        self.required_properties = required_properties

    def validate(self, value: dict, context: Context = Context()):
        for property_name in self.required_properties:
            if property_name not in value:
                raise RequiredPropertyValidationError(path=context.path, expected_property=property_name)

    def __repr__(self) -> str:
        return f"validate_required({self.required_properties})"


class MinimumPropertiesValidator(Validator):
    def __init__(self, expected_minimum: int):
        self.expected_minimum = expected_minimum

    def validate(self, value, context: Context = Context()) -> None:
        if len(value) < self.expected_minimum:
            raise MinimumPropertiesValidationError(path=context.path, expected_minimum=self.expected_minimum)


class MaximumPropertiesValidator(Validator):
    def __init__(self, expected_maximum: int):
        self.expected_maximum = expected_maximum

    def validate(self, value, context: Context = Context()) -> None:
        if len(value) > self.expected_maximum:
            raise MaximumPropertiesValidationError(path=context.path, expected_maximum=self.expected_maximum)


class ObjectValidator(CompoundValidator):
    additional_properties: CompoundValidator = None
    pattern_properties: CompoundValidator = None
    unevaluated_properties: CompoundValidator = None
    property_names: CompoundValidator = None

    def __init__(self):
        self._patterns: Dict[str, Pattern] = {}
        super().__init__()

    def validate(self, value, context: Context = Context()):
        if not isinstance(value, dict):
            return

        for item_key, item_value in value.items():
            if self.property_names:
                self.property_names.validate(item_key, context + item_key)

            evaluated = False
            if item_key in self:
                self[item_key].validate(item_value, context + item_key)
                continue

            if self.pattern_properties:
                for pattern, pattern_validator in self.pattern_properties.items():
                    if re.search(pattern, item_key):
                        pattern_validator.validate(item_value, context + item_key)
                        evaluated = True

            if evaluated:
                continue

            if self.additional_properties:
                self.additional_properties.validate(item_value, context + item_key)
                continue

            if self.unevaluated_properties:
                self.unevaluated_properties.validate(item_value, context + item_key)


class DependentRequiredValidator(Validator):
    def __init__(self, dependent_map: Dict[str, List[str]]):
        self._map = dependent_map
        super().__init__()

    def validate(self, value, context: Context = Context()) -> None:
        if not isinstance(value, dict):
            return

        for key, items in self._map.items():
            if key not in value:
                continue

            for item in items:
                if item in value:
                    continue

                raise DependentValidationError(property=key, expected_property=item, path=context.path)


class DependentSchemasValidator(CompoundValidator):
    def validate(self, value, context: Context = Context()) -> None:
        if not isinstance(value, dict):
            return

        for key, validator in self._data.items():
            if key not in value:
                continue

            validator.validate(value, context)
