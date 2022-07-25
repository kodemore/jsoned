from __future__ import annotations

from functools import lru_cache, partial
from hashlib import sha256
from typing import Dict, overload, Optional
from typing import List, Union

from .json_core import JsonSchema as BaseJsonSchema, can_apply_keyword, Vocabulary, ApplicatorKeyword, Keyword
from .json_pointer import JsonPointer
from .types.json_complex import JsonObject, JsonArray
from .types.json_boolean import JsonBoolean
from .types.json_type import JsonType
from .uri import Uri
from .utils import AnyJsonType
from .validators.core_validators import Validator, ValidatorsMap, Context
from .validators.deferred_validator import deferred_validator

__all__ = ["JsonSchema"]


class JsonSchema(BaseJsonSchema):
    def __init__(self, value: Union[JsonObject, JsonArray, Dict[str, AnyJsonType], List[AnyJsonType]], vocabulary: List[Keyword] = None):
        if not isinstance(value, (dict, list, bool, JsonObject, JsonArray, JsonBoolean)):
            raise ValueError(f"JsonSchema.__init__ accepts dict, list, JsonObject or JsonArray `{value!r}` given instead.")

        if isinstance(value, dict):
            value = JsonObject(value)
        elif isinstance(value, list):
            value = JsonArray(value)
        elif isinstance(value, bool):
            value = JsonBoolean(value)

        self._value: JsonType = value
        self.ready = False
        self._validator: Optional[Validator] = None
        self._vocabulary = vocabulary if vocabulary is not None else []
        self.anchors: Dict[str, JsonType] = {}
        self._id = None

    @property
    def vocabulary(self) -> Vocabulary:
        return self._vocabulary

    @property
    def validator(self) -> Validator:
        self.load()

        if self._validator is None:
            self._validator = partial(deferred_validator, schema=self, node=self._value)

        return self._validator

    def validate(self, value: AnyJsonType, context: Context = None) -> bool:
        context = context or Context()
        return self.validator(value, context)

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
        self.ready = True
        # process applicator keywords only on-load
        self._value = self._process_node(
            self._value,
            [keyword for keyword in self.vocabulary if isinstance(keyword, ApplicatorKeyword)]
        )

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

    def _process_node(self, node: JsonType, keywords: Vocabulary) -> JsonType:
        if node.type == JsonType.ARRAY:
            node._value = [
                self._process_node(value, keywords) for value in node
            ]
            return node
        elif node.type != JsonType.OBJECT:
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
