from __future__ import annotations

from decimal import Decimal
from enum import Enum
from functools import cached_property, lru_cache
from typing import Union, overload, Any, List, Set

__all__ = ["ValidationError"]


class ValidationError(ValueError):
    class ErrorCodes(Enum):
        ERROR = "error"
        EQUAL_ERROR = "equal_error"
        ENUM_ERROR = "enum_error"
        TYPE_ERROR = "type_error"

        ANY_OF_ERROR = "any_of_error"
        NOT_ERROR = "not_error"
        ONE_OF_ERROR = "one_of_error"

        NUMBER_MINIMUM_ERROR = "number_minimum_error"
        NUMBER_EXCLUSIVE_MINIMUM_ERROR = "number_exclusive_minimum_error"
        NUMBER_MAXIMUM_ERROR = "number_maximum_error"
        NUMBER_EXCLUSIVE_MAXIMUM_ERROR = "number_exclusive_maximum_error"
        NUMBER_MULTIPLE_OF_ERROR = "number_multiple_of_error"

        STRING_MINIMUM_LENGTH_ERROR = "string_minimum_length_error"
        STRING_MAXIMUM_LENGTH_ERROR = "string_maximum_length_error"
        STRING_FORMAT_ERROR = "string_format_error"
        STRING_PATTERN_ERROR = "string_pattern_error"

        PROPERTY_UNEVALUATED_ERROR = "property_unevaluated_error"
        PROPERTY_MISSING_ERROR = "property_missing_error"
        PROPERTY_MINIMUM_LENGTH_ERROR = "property_minimum_length_error"
        PROPERTY_MAXIMUM_LENGTH_ERROR = "property_maximum_length_error"
        PROPERTY_INVALID_NAME_ERROR = "property_invalid_name_error"
        PROPERTY_UNEXPECTED_ADDITIONAL_PROPERTY_ERROR = "property_unexpected_additional_property_error"

        ARRAY_MIN_CONTAINS_ERROR = "array_min_contains_error"
        ARRAY_MAX_CONTAINS_ERROR = "array_min_contains_error"
        ARRAY_ADDITIONAL_ITEMS_ERROR = "array_additional_items_error"
        ARRAY_NON_UNIQUE_ERROR = "array_non_unique_error"
        ARRAY_MIN_LENGTH_ERROR = "array_minimum_length_error"
        ARRAY_MAX_LENGTH_ERROR = "array_maximum_length_error"

        def __str__(self) -> str:
            return self.value

        def __repr__(self) -> str:
            return f"`{self.value}`"

    def __init__(self, path: str, message: str = "Validation failed.", code: Union[ErrorCodes, str] = ErrorCodes.ERROR, **kwargs):
        self._message = message
        self._code = code
        self._path = path
        self._data = kwargs

        self._data["path"] = self.path
        self._data["code"] = self.code

        super().__init__(str(self))

    @overload
    def __getitem__(self, key: str) -> Any:
        ...

    def __getitem__(self, key):
        if key in self._data:
            return self._data[key]

    @property
    def message(self) -> str:
        return self._message

    @cached_property
    def code(self) -> ValidationError.ErrorCodes:
        return self._code

    @property
    def path(self) -> str:
        return self._path

    def __bool__(self) -> bool:
        return False

    @lru_cache
    def __str__(self) -> str:
        return self.message.format(**self._data)

    @classmethod
    def for_any_of(cls, path: str, error_codes: Set[ErrorCodes]) -> ValidationError:
        return cls(
            message="Passed value could not validate against any expected schema. Failed with: {error_codes}",
            code=ValidationError.ErrorCodes.ANY_OF_ERROR,
            path=path,
            error_codes=error_codes,
        )

    @classmethod
    def for_one_of(cls, path: str) -> ValidationError:
        return cls(
            message="Passed value could not validate against expected schema, `anyOf` condition failed.",
            code=ValidationError.ErrorCodes.ONE_OF_ERROR,
            path=path,
        )

    @classmethod
    def for_equal(cls, path: str, expected_value: Any) -> ValidationError:
        return cls(
            message="Passed value must equal to `{expected_value}`.",
            code=ValidationError.ErrorCodes.EQUAL_ERROR,
            path=path,
            expected_value=expected_value,
        )

    @classmethod
    def for_enum(cls, path: str, expected_values: List[Union[str, Decimal, int, bool]]) -> ValidationError:
        return cls(
            message="Passed value must match one of the following values `{expected_values}`.",
            code=ValidationError.ErrorCodes.ENUM_ERROR,
            path=path,
            expected_values=expected_values,
        )

    @classmethod
    def for_type(cls, path: str, expected_types: List[str]) -> ValidationError:
        return cls(
            message="Passed value must be one of the following type(s) `{expected_types}`.",
            code=ValidationError.ErrorCodes.TYPE_ERROR,
            path=path,
            expected_types=expected_types
        )

    @classmethod
    def for_number_minimum(cls, path: str, expected_minimum: Decimal) -> ValidationError:
        return cls(
            message="Passed value must be greater or equal to `{expected_minimum}`.",
            code=ValidationError.ErrorCodes.NUMBER_MINIMUM_ERROR,
            path=path,
            expected_minimum=expected_minimum,
        )

    @classmethod
    def for_number_exclusive_minimum(cls, path: str, expected_minimum: Decimal) -> ValidationError:
        return cls(
            message="Passed value must be greater than `{expected_minimum}`.",
            code=ValidationError.ErrorCodes.NUMBER_EXCLUSIVE_MINIMUM_ERROR,
            path=path,
            expected_minimum=expected_minimum,
        )

    @classmethod
    def for_number_maximum(cls, path: str, expected_maximum: Decimal) -> ValidationError:
        return cls(
            message="Passed value must be lower or equal to `{expected_maximum}`.",
            code=ValidationError.ErrorCodes.NUMBER_MAXIMUM_ERROR,
            path=path,
            expected_maximum=expected_maximum,
        )

    @classmethod
    def for_number_exclusive_maximum(cls, path: str, expected_maximum: Decimal) -> ValidationError:
        return cls(
            message="Passed value must be lower than `{expected_maximum}`.",
            code=ValidationError.ErrorCodes.NUMBER_EXCLUSIVE_MAXIMUM_ERROR,
            path=path,
            expected_maximum=expected_maximum,
        )

    @classmethod
    def for_number_multiple_of(cls, path: str, multiple_of: Decimal) -> ValidationError:
        return cls(
            message="Passed value must be multiplication of `{multiple_of}`.",
            code=ValidationError.ErrorCodes.NUMBER_MULTIPLE_OF_ERROR,
            path=path,
            multiple_of=multiple_of,
        )

    @classmethod
    def for_string_minimum_length(cls, path: str, expected_minimum: int) -> ValidationError:
        return cls(
            message="Passed value must be at least `{expected_minimum}` characters long.",
            code=ValidationError.ErrorCodes.STRING_MINIMUM_LENGTH_ERROR,
            path=path,
            expected_minimum=expected_minimum,
        )

    @classmethod
    def for_string_maximum_length(cls, path: str, expected_maximum: int) -> ValidationError:
        return cls(
            message="Passed value cannot exceed `{expected_maximum}` characters.",
            code=ValidationError.ErrorCodes.STRING_MAXIMUM_LENGTH_ERROR,
            path=path,
            expected_maximum=expected_maximum,
        )

    @classmethod
    def for_string_pattern(cls, path: str, expected_pattern: str) -> ValidationError:
        return cls(
            message="Passed value must follow `{expected_pattern}` pattern.",
            code=ValidationError.ErrorCodes.STRING_PATTERN_ERROR,
            path=path,
            expected_pattern=expected_pattern,
        )

    @classmethod
    def for_string_format(cls, path: str, expected_format: str) -> ValidationError:
        return cls(
            message="Passed value must conform `{expected_format}` format.",
            code=ValidationError.ErrorCodes.STRING_FORMAT_ERROR,
            path=path,
            expected_format=expected_format,
        )

    @classmethod
    def for_unevaluated_property(cls, path: str, property_name: str) -> ValidationError:
        return cls(
            message="Unevaluated property `{property_name}` detected.",
            code=ValidationError.ErrorCodes.PROPERTY_UNEVALUATED_ERROR,
            path=path,
            property_name=property_name,
        )

    @classmethod
    def for_missing_property(cls, path: str, property_name: str) -> ValidationError:
        return cls(
            message="Property `{property_name}` is required.",
            code=ValidationError.ErrorCodes.PROPERTY_MISSING_ERROR,
            path=path,
            property_name=property_name,
        )

    @classmethod
    def for_additional_property(cls, path: str, property_name: str) -> ValidationError:
        return cls(
            message="Property `{property_name}` is not allowed, object does not accept additional properties.",
            code=ValidationError.ErrorCodes.PROPERTY_UNEXPECTED_ADDITIONAL_PROPERTY_ERROR,
            path=path,
            property_name=property_name,
        )

    @classmethod
    def for_property_name(cls, path: str, property_name: str, reason: ValidationError) -> ValidationError:
        return cls(
            message="Property `{property_name}` is not matching expected naming schema: `{reason}`",
            code=ValidationError.ErrorCodes.PROPERTY_INVALID_NAME_ERROR,
            path=path,
            property_name=property_name,
            reason=reason,
        )

    @classmethod
    def for_property_minimum_length(cls, path: str, expected_minimum: int) -> ValidationError:
        return cls(
            message="Object should contain at least  `{expected_minimum}` property/ies.",
            code=ValidationError.ErrorCodes.PROPERTY_MINIMUM_LENGTH_ERROR,
            path=path,
            expected_minimum=expected_minimum,
        )

    @classmethod
    def for_property_maximum_length(cls, path: str, expected_maximum: int) -> ValidationError:
        return cls(
            message="Object should contain at most `{expected_maximum}` property/ies.",
            code=ValidationError.ErrorCodes.PROPERTY_MAXIMUM_LENGTH_ERROR,
            path=path,
            expected_maximum=expected_maximum,
        )

    @classmethod
    def for_array_minimum_contains(cls, path: str, expected_minimum: int) -> ValidationError:
        return cls(
            message="Array should contain at least `{expected_minimum}` time/s of specified item.",
            code=ValidationError.ErrorCodes.ARRAY_MIN_CONTAINS_ERROR,
            path=path,
            expected_minimum=expected_minimum,
        )

    @classmethod
    def for_array_maximum_contains(cls, path: str, expected_maximum: int) -> ValidationError:
        return cls(
            message="Array should contain at max `{expected_maximum}` time/s of specified item.",
            code=ValidationError.ErrorCodes.ARRAY_MAX_CONTAINS_ERROR,
            path=path,
            expected_maximum=expected_maximum,
        )

    @classmethod
    def for_array_non_unique(cls, path: str) -> ValidationError:
        return cls(
            message="Array expected to be unique",
            code=ValidationError.ErrorCodes.ARRAY_NON_UNIQUE_ERROR,
            path=path,
        )

    @classmethod
    def for_array_minimum_length(cls, path: str, expected_minimum: int) -> ValidationError:
        return cls(
            message="Array should contain at least `{expected_minimum}` elements.",
            code=ValidationError.ErrorCodes.ARRAY_MIN_LENGTH_ERROR,
            path=path,
            expected_minimum=expected_minimum,
        )

    @classmethod
    def for_array_maximum_length(cls, path: str, expected_maximum: int) -> ValidationError:
        return cls(
            message="Array should contain at max `{expected_maximum}` elements.",
            code=ValidationError.ErrorCodes.ARRAY_MAX_LENGTH_ERROR,
            path=path,
            expected_maximum=expected_maximum,
        )

    @classmethod
    def for_array_additional_items(cls, path: str, index: int) -> ValidationError:
        return cls(
            message="Array should not contain additional items, additional item at index `{index}` found.",
            code=ValidationError.ErrorCodes.ARRAY_ADDITIONAL_ITEMS_ERROR,
            path=path,
            index=index,
        )

    @classmethod
    def for_not(cls, path: str) -> ValidationError:
        return cls(
            message="Passed value could not validate against expected schema, `not` condition failed.",
            code=ValidationError.ErrorCodes.NOT_ERROR,
            path=path,
        )
