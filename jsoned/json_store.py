from __future__ import annotations

from functools import partial
from json import load as _load_json
from os import path
from typing import overload, Dict, List

from yaml import FullLoader as YamlFullLoader, load as load_yaml

from .json_core import JsonDocument, JsonLoader, Keyword
from .keywords import RefKeyword, AnchorKeyword
from .uri import Uri
from .uri_resolver import UriResolver
from .utils import AnyJsonType

_load_yaml = partial(load_yaml, Loader=YamlFullLoader)

__all__ = ["JsonStore"]


_SUPPORTED_FORMATS = {
    ".yaml": _load_yaml,
    ".yml": _load_yaml,
    ".json": _load_json,
}


class JsonStore(JsonLoader):
    _instance: JsonStore = None

    def __init__(self, keywords: List[Keyword] = None):
        self._cache: Dict[str, JsonDocument] = {}
        self.resolver = UriResolver()
        self.keywords = keywords if keywords is not None else []

    def add(self, uri: Uri, document: JsonDocument) -> None:
        self._cache[str(uri.base_uri)] = document

    @overload
    def load(self, uri: Uri) -> JsonDocument:
        ...

    @overload
    def load(self, file: str) -> JsonDocument:
        ...

    def load(self, obj) -> JsonDocument:
        if isinstance(obj, Uri):
            return self.load_uri(obj)
        if isinstance(obj, str):
            return self.load_file(obj)

        raise ValueError(
            f"JsonStore.load() expects `obj` argument to be one of: `JsonUri`, `str`, `{type(obj)}` given."
        )

    def load_uri(self, uri: Uri) -> JsonDocument:
        base_uri = str(uri.base_uri)
        if base_uri in self._cache:
            return self._cache[base_uri]

        document = self.load_file(self.resolver.resolve(uri))
        self._cache[base_uri] = document

        return document

    def load_file(self, filename: str) -> JsonDocument:
        if filename in self._cache:
            return self._cache[filename]

        file = open(filename, "r")
        _, extension = path.splitext(file.name)
        if extension not in _SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported file format `{extension}`, expected `json` or `yaml`.")

        json = _SUPPORTED_FORMATS[extension](file)
        document = JsonDocument(json, self.keywords)
        self._cache[filename] = document

        return document

    @classmethod
    def default(cls) -> JsonStore:
        if cls._instance is None:
            cls._instance = cls()
            cls._instance.keywords.append(RefKeyword(cls._instance))
            cls._instance.keywords.append(AnchorKeyword())

        return cls._instance
