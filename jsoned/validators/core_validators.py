from __future__ import annotations

from abc import abstractmethod
from collections import OrderedDict
from collections.abc import Iterable
from decimal import Decimal
from enum import Enum
from functools import partial
from typing import Any, List, overload, Dict, Tuple, Callable, Iterator, Mapping, Collection, \
    Generic, TypeVar, Union

from jsoned.errors import ValidationError


class Context:
    def __init__(self, parent: Context = None):
        self._data = {}
        self._errors: List[ValidationError] = []
        self._path: Tuple[str] = tuple()
        self._parent = parent

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

    @property
    def errors(self) -> List[ValidationError]:
        return self._errors

    @property
    def path(self) -> str:
        return ".".join(self._path)

    def __add__(self, key: str) -> Context:
        context = Context(self)
        context._path = self._path + tuple([key])
        context._data = self._data
        context._errors = self._errors

        return context

    def fork(self) -> Context:
        context = Context(self)
        context._path = self._path
        context._data = self._data

        return context

    def with_path(self) -> Context:
        context = Context()
        context._path = self._path

        return context


Validator = Union[Callable[[Any, Context], bool], partial[bool]]


class ValidatorsIterable(Iterable):
    @overload
    def __iter__(self) -> Iterator[Validator]:
        ...

    @abstractmethod
    def __iter__(self):
        ...

    @abstractmethod
    def __bool__(self) -> bool:
        ...

    @abstractmethod
    def items(self) -> Iterator:
        ...

    @abstractmethod
    def __getitem__(self, item) -> Validator:
        ...


class ValidatorsCollection(Collection, ValidatorsIterable):
    def __init__(self, data: List[Validator] = None):
        self._data = data or []

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    @overload
    def __getitem__(self, i: int) -> Validator:
        ...

    @overload
    def __getitem__(self, i: slice) -> ValidatorsCollection:
        ...

    def __getitem__(self, i):
        if isinstance(i, slice):
            return self.__class__(self._data[i])
        else:
            return self._data[i]

    def __setitem__(self, i, item):
        self._data[i] = item

    def append(self, item: Validator, **kwargs) -> None:
        if kwargs:
            self._data.append(partial(item, **kwargs))
            return
        self._data.append(item)

    @overload
    def __contains__(self, item: Validator) -> bool:
        ...

    def __contains__(self, item):
        return item in self._data

    def __bool__(self) -> bool:
        return len(self._data) > 0

    def items(self):
        return enumerate(self._data)


T = TypeVar('T')


class ValidatorsMap(Mapping, ValidatorsIterable, Generic[T]):
    __slots__ = ["_data"]

    def __init__(self):
        self._data: Dict[T, Validator] = OrderedDict()

    @overload
    def __setitem__(self, key: T, value: Validator) -> None:
        ...

    def __setitem__(self, key, value):
        self._data[key] = value

    @overload
    def __getitem__(self, key: T) -> Validator:
        ...

    def __getitem__(self, key):
        return self._data[key]

    @overload
    def __contains__(self, key: T) -> bool:
        ...

    def __contains__(self, key):
        return key in self._data

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self):
        return iter(self._data.values())

    def __bool__(self) -> bool:
        return len(self._data) > 0

    def items(self) -> Iterable[Tuple[str, Callable]]:
        return self._data.items()

    def keys(self) -> Iterable[str]:
        return self._data.keys()

    def values(self) -> Iterable[Callable]:
        return self._data.values()


class AssertType(Enum):
    STRING = "string"
    INTEGER = "integer"
    NUMBER = "number"
    BOOLEAN = "boolean"
    ARRAY = "array"
    OBJECT = "object"
    NULL = "null"

    def __str__(self) -> str:
        return self.value


_TYPE_MAP: Dict[TypeVar, AssertType] = {
    str: AssertType.STRING,
    int: AssertType.INTEGER,
    float: AssertType.NUMBER,
    Decimal: AssertType.NUMBER,
    bool: AssertType.BOOLEAN,
    list: AssertType.ARRAY,
    dict: AssertType.OBJECT,
    type(None): AssertType.NULL,
}


def validate_type(value, context: Context, expected_types: List[AssertType]) -> bool:
    value_type = type(value)
    if value_type not in _TYPE_MAP:
        context.errors.append(ValidationError.for_type(path=context.path, expected_types=[str(item) for item in expected_types]))
        return False

    assert_type = _TYPE_MAP[value_type]
    if assert_type in expected_types:
        return True

    if assert_type == AssertType.INTEGER and AssertType.NUMBER in expected_types:
        return True

    context.errors.append(ValidationError.for_type(path=context.path, expected_types=[str(item) for item in expected_types]))
    return False


def pass_validation(value, context: Context) -> bool:
    return True


def fail_validation(value, context: Context) -> bool:
    context.errors.append(ValidationError(context.path))
    return False


def validate_enum(value, context: Context, expected_values: List[Union[str, Decimal, int, bool]]) -> bool:
    for item in expected_values:
        try:
            if value != item:
                continue
        except TypeError:
            continue

        return True

    context.errors.append(ValidationError.for_enum(context.path, expected_values=expected_values))
    return False


def validate_const(value, context: Context, expected_value: Any) -> bool:
    try:
        if value != expected_value:
            context.errors.append(ValidationError.for_equal(context.path, expected_value=expected_value))
            return False
    except TypeError:
        context.errors.append(ValidationError.for_equal(context.path, expected_value=expected_value))
        return False

    return True
