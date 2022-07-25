from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Union
from typing import Protocol

from .types.json_complex import JsonObject
from .types.json_type import JsonType
from .uri import Uri
from .utils import AnyJsonType
from .validators.core_validators import Validator, ValidatorsMap, Context

__all__ = ["JsonSchema", "Keyword", "ApplicatorKeyword", "AssertionKeyword", "Vocabulary", "can_apply_keyword"]


class Keyword(ABC):
    key: Union[str, List[str]]

    @abstractmethod
    def apply(self, *args, **kwargs):
        ...


class ApplicatorKeyword(Keyword, ABC):
    """
    Applies one or more sub-schemas to a particular location in the instance, and combine or modify their results.
    """

    @abstractmethod
    def apply(self, document: JsonSchema, node: JsonObject) -> JsonType:
        ...


class AssertionKeyword(Keyword, ABC):
    """
    Validates value against schema.
    """

    @abstractmethod
    def apply(self, document: JsonSchema, node: JsonObject, validator: ValidatorsMap):
        ...


def can_apply_keyword(node: JsonObject, keyword: Keyword) -> bool:
    key = keyword.key

    # Invalid key type
    if not isinstance(key, (str, list)):
        return False

    # Key is not within a value
    if isinstance(key, str) and key not in node:
        return False

    # Key is a list but is not within a value
    if isinstance(key, list) and not any(i in node for i in key):
        return False

    return True


Vocabulary = List[Keyword]


class JsonSchema(Protocol):
    @property
    @abstractmethod
    def vocabulary(self) -> Vocabulary:
        ...

    @property
    @abstractmethod
    def validator(self) -> Validator:
        ...

    @abstractmethod
    def validate(self, value: AnyJsonType, context: Context = None) -> bool:
        ...

    @property
    @abstractmethod
    def id(self) -> Uri:
        ...

    @id.setter
    @abstractmethod
    def id(self, value: Uri) -> None:
        ...

    @property
    @abstractmethod
    def value(self) -> JsonType:
        ...

    @abstractmethod
    def query(self, query) -> JsonType:
        ...
