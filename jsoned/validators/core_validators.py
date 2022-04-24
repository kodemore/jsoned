from __future__ import annotations

from abc import abstractmethod, ABC
from decimal import Decimal
from typing import Any, List, overload, Dict, Tuple

from jsoned.errors import ValidationError
from jsoned.errors.core_validation_errors import TypeValidationError, EnumValidationError, ConstValidationError
from jsoned.types import JsonType
from jsoned.utils import AnyJsonType


class Context:
    def __init__(self):
        self._data = {}
        self._path: Tuple[str] = tuple()

    def __getitem__(self, key: str) -> None:
        return self._data[key]

    def __setitem__(self, key: str, value):
        self._data[key] = value

    def __contains__(self, key: str):
        return key in self._data

    def items(self):
        return self._data.items()

    def keys(self):
        return self._data.keys()

    def __repr__(self):
        return f"Context({self.path})"

    @property
    def path(self) -> str:
        return ".".join(self._path)

    def __add__(self, key: str) -> Context:
        context = Context()
        context._path = self._path + tuple([key])

        return context


class Validator(ABC):
    @abstractmethod
    def validate(self, value, context: Context = Context()) -> None:
        ...

    def __call__(self, value: AnyJsonType, context: Context = Context()):
        self.validate(value, context)

    def __repr__(self) -> str:
        return f"validate"


class CompoundValidator(Validator):
    def __init__(self):
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

    def values(self):
        return self._data.values()

    def validate(self, value, context: Context = Context()) -> None:
        for validator in self.values():
            validator(value, context)

    def __call__(self, value: AnyJsonType, context: Context = Context()):
        self.validate(value, context)

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

    def __init__(self, expected_types: List[str]):
        self._expected_types = expected_types

    def validate(self, value, context: Context = Context()) -> None:
        value_type = type(value)
        if value_type not in self.TYPE_MAP:
            raise TypeValidationError(expected_types=self._expected_types, path=context.path)

        asserted_type = self.TYPE_MAP[value_type]
        if asserted_type not in self._expected_types:
            raise TypeValidationError(expected_types=self._expected_types, path=context.path)

    def __repr__(self) -> str:
        return f"validate_type({self._expected_types})"


class PassValidator(Validator):
    def validate(self, value, context: Context = Context()) -> None:
        return


class FailValidator(Validator):
    def validate(self, value, context: Context = Context()) -> None:
        raise ValidationError(f"Unexpected `{value}` value passed.", path=context.path)


class EnumValidator(Validator):
    def __init__(self, expected_values: List[Any]):
        self._contains_booleans = False
        self._expected_values = []

        for value in expected_values:
            if isinstance(value, JsonType):
                value = value.value

            if type(value) == bool:
                self._contains_booleans = True
            self._expected_values.append(value)

    def validate(self, value, context: Context = Context()) -> None:
        if type(value) == bool and not self._contains_booleans:
            raise EnumValidationError(expected_values=self._expected_values, path=context.path)

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

            raise EnumValidationError(expected_values=self._expected_values, path=context.path)

        # normal scenario
        if value in self._expected_values:
            return value

        raise EnumValidationError(expected_values=self._expected_values, path=context.path)

    def __repr__(self) -> str:
        return f"validate_enum({self._expected_values})"


class ConstValidator(Validator):
    def __init__(self, expected_value: Any):
        self.expected_value = expected_value

    def validate(self, value, context: Context = Context()) -> None:
        if (isinstance(self.expected_value, bool) or isinstance(value, bool)) and type(value) != type(self.expected_value):
            raise ConstValidationError(expected_value=self.expected_value, path=context.path)

        if value != self.expected_value:
            raise ConstValidationError(expected_value=self.expected_value, path=context.path)
