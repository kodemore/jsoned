from __future__ import annotations

from abc import abstractmethod, ABC
from decimal import Decimal
from functools import cached_property
from typing import Any, List, overload, Dict

from jsoned.errors.core_validation_errors import TypeValidationError, EnumValidationError
from jsoned.types import JsonType
from jsoned.utils import AnyJsonType


class Validator(ABC):
    def __init__(self, key: str = "", parent: Validator = None):
        self._key = key
        self._parent = parent

    @cached_property
    def path(self) -> str:
        if self._parent and self._parent._key != "":
            return f"{self._parent._key}{self._key}"

        return self._key if self._key else ""

    @abstractmethod
    def validate(self, value, ) -> None:
        ...

    def __call__(self, value: AnyJsonType):
        self.validate(value)

    def __repr__(self) -> str:
        return f"validate"


class CompoundValidator(Validator):
    def __init__(self, key: str = "", parent: Validator = None):
        super().__init__(key, parent)
        self._data: Dict[str, Validator] = {}

    @overload
    def __setitem__(self, key: str, value: Validator) -> None:
        ...

    def __setitem__(self, key, value) -> None:
        self._data[key] = value

    @overload
    def __getitem__(self, key: str) -> Validator:
        ...

    def __getitem__(self, key):
        return self._data[key]

    def __contains__(self, key):
        return key in self._data

    def items(self):
        return self._data.items()

    def validate(self, value: AnyJsonType):
        for key, validator in self.items():
            validator(value)

    def __call__(self, value: AnyJsonType):
        self.validate(value)

    def __repr__(self) -> str:
        return f"validate({self._data})"


class TypeValidator(Validator):
    TYPE_MAP = {
        str: "string",
        int: "integer",
        float: "number",
        Decimal: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
        type(None): "null",
    }

    def __init__(self, expected_types: List[str], key: str = "@type", parent: Validator = None):
        super().__init__(key, parent)
        self._expected_types = expected_types

    def validate(self, value) -> None:
        value_type = type(value)
        if value_type not in self.TYPE_MAP:
            raise TypeValidationError(expected_types=self._expected_types, path=self.path)

        asserted_type = self.TYPE_MAP[value_type]
        if asserted_type not in self._expected_types:
            raise TypeValidationError(expected_types=self._expected_types, path=self.path)

    def __repr__(self) -> str:
        return f"validate_type({self._expected_types})"


class EnumValidator(Validator):
    def __init__(self, expected_values: List[Any], key: str = "@enum", parent: Validator = None):
        super().__init__(key, parent)
        self._contains_booleans = False
        self._expected_values = []

        for value in expected_values:
            if isinstance(value, JsonType):
                value = value.value

            if type(value) == bool:
                self._contains_booleans = True
            self._expected_values.append(value)

    def validate(self, value) -> None:
        if type(value) == bool and not self._contains_booleans:
            raise EnumValidationError(expected_values=self._expected_values, path=self.path)

        # tweak for bool checking
        if self._contains_booleans and value == 1 or value == 0:
            for item in self._expected_values:
                if item == value:
                    if type(item) == bool or type(value) == bool:
                        if type(item) == type(value):
                            return
                        else:
                            continue
                    return

            raise EnumValidationError(expected_values=self._expected_values, path=self.path)

        # normal scenario
        if value in self._expected_values:
            return value

        raise EnumValidationError(expected_values=self._expected_values, path=self.path)

    def __repr__(self) -> str:
        return f"validate_enum({self._expected_values})"
