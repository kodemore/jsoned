from __future__ import annotations

from abc import ABC, abstractmethod
from functools import lru_cache
from hashlib import sha256
from typing import Dict, overload, Any, Optional
from typing import List, Union

from .json_pointer import JsonPointer
from .types.json_complex import JsonObject, JsonArray
from .types.json_type import JsonType
from .uri import Uri
from .utils import AnyJsonType
from .validators.core_validators import CompoundValidator

__all__ = ["build_validator_for_node", "JsonSchema", "Keyword", "ApplicatorKeyword", "AssertionKeyword", "Vocabulary"]


class Keyword(ABC):
    key: Union[str, List[str]]


Vocabulary = List[Keyword]


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
    def apply(self, document: JsonSchema, node: JsonObject, validator: CompoundValidator) -> CompoundValidator:
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


def build_validator_for_node(schema: JsonSchema, node: Union[JsonObject, JsonType], validator: CompoundValidator) -> CompoundValidator:
    for keyword in schema.vocabulary:
        if not isinstance(keyword, AssertionKeyword):
            continue

        if not can_apply_keyword(node, keyword):
            continue

        validator = keyword.apply(schema, node, validator)

    return validator


class JsonSchema:
    def __init__(self, value: Union[JsonObject, JsonArray, Dict[str, AnyJsonType], List[AnyJsonType]], vocabulary: List[Keyword] = None):
        if not isinstance(value, (dict, list, JsonObject, JsonArray)):
            raise ValueError(f"JsonSchema.__init__ accepts dict, list, JsonObject or JsonArray `{value!r}` given instead.")

        if isinstance(value, dict):
            value = JsonObject(value)
        elif isinstance(value, list):
            value = JsonArray(value)

        self._value: JsonType = value
        self.ready = False
        self._validator: Optional[CompoundValidator] = None
        self.vocabulary = vocabulary if vocabulary is not None else []
        self.anchors: Dict[str, JsonType] = {}
        self._id = None

    @property
    def validator(self) -> CompoundValidator:
        self.load()

        if self._validator is None:
            if self._value.type != JsonType.OBJECT:
                self._validator = CompoundValidator()
            else:
                self._validator = self._build_validator()

        return self._validator

    def validate(self, value: AnyJsonType) -> Any:
        return self.validator.validate(value)

    def _build_validator(self) -> CompoundValidator:
        return build_validator_for_node(self, self._value, CompoundValidator())

    @property
    def id(self):
        if self._id:
            return self._id

        doc_sha = sha256(repr(self._value).encode("utf8")).hexdigest()
        self._id: Uri = Uri(f"local://{doc_sha}/")

        return self._id

    @id.setter
    def id(self, value: Uri) -> None:
        self._id = value

    @property
    def value(self) -> JsonType:
        if self.ready:
            return self._value
        self.load()
        return self._value

    def load(self) -> None:
        if self.ready:
            return

        # process applicator keywords only on-load
        self._value = self._process_node(
            self._value,
            [keyword for keyword in self.vocabulary if isinstance(keyword, ApplicatorKeyword)]
        )

        self.ready = True

    @overload
    def query(self, query: str) -> JsonType:
        ...

    @overload
    def query(self, pointer: JsonPointer) -> JsonType:
        ...

    @lru_cache()
    def query(self, query) -> JsonType:

        if isinstance(query, str):
            pointer = JsonPointer(query)
        elif isinstance(query, JsonPointer):
            pointer = query
        else:
            raise ValueError(
                f"Query must be either `str` or `JsonPointer`, `{type(query)}` given instead."
            )
        node = self.value

        if len(pointer) == 1 and pointer[0] in self.anchors:
            return self.anchors[pointer[0]]

        if len(pointer) == 1 and pointer[0] == "":
            return node

        visited = []
        for key in pointer:
            if node.type == JsonType.ARRAY:
                node = node[int(key)]
            elif node.type == JsonType.OBJECT:
                node = node[key]
            else:
                raise KeyError(
                    f"Could not resolve `{key}` in reference `{pointer}` at `{JsonPointer.from_list(visited)}`"
                )

            visited.append(key)
        return node

    def _process_node(self, node: JsonType, keywords: List[Keyword]) -> JsonType:
        if node.type != JsonType.OBJECT:
            return node

        node._value = {
            key: self._process_node(value, keywords) for key, value in node.items()
        }

        for keyword in keywords:
            if not can_apply_keyword(node, keyword):
                continue

            try:
                node = keyword.apply(self, node)
            except Exception as e:
                raise e

        return node

    def __repr__(self) -> str:
        return f"JsonSchema({self._value})"
