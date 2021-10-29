from __future__ import annotations

from functools import partial
from json import load as _load_json
from typing import overload, Dict

from yaml import FullLoader as YamlFullLoader, load as load_yaml

from jsoned.json_uri import JsonUri
from .json_core import JsonDocument, JsonLoader
from .json_uri_resolver import JsonUriResolver

_load_yaml = partial(load_yaml, Loader=YamlFullLoader)

__all__ = ["JsonStore"]


_SUPPORTED_FORMATS = {
    "yaml": _load_yaml,
    "json": _load_json,
}


class JsonStore(JsonLoader):

    _instance: JsonStore = None

    def __init__(self):
        self._cache: Dict[str, JsonDocument] = {}
        self.resolver = JsonUriResolver()

    def add(self, uri: JsonUri, document: JsonDocument) -> None:
        self._cache[uri.base_uri] = document

    @overload
    def load(self, uri: JsonUri) -> JsonDocument:
        ...

    @overload
    def load(self, file: str) -> JsonDocument:
        ...

    @overload
    def load(self, doc: dict) -> JsonDocument:
        ...

    def load(self, obj) -> JsonDocument:
        if isinstance(obj, JsonUri):
            return self.load_uri(obj)
        if isinstance(obj, str):
            return self.load_file(obj)
        if isinstance(obj, dict):
            return self.load_dict(obj)

        raise ValueError(f"JsonStore.load() expects `obj` argument to be one of: `dict`, `JsonUri`, `str`, `{type(obj)}` given.")

    def load_uri(self, uri: JsonUri) -> JsonDocument:
        ...

    def load_file(self, path: str) -> JsonDocument:
        ...

    def load_dict(self, obj: dict) -> JsonDocument:
        ...

    @classmethod
    def default(cls) -> JsonStore:
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance
