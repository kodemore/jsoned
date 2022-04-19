from __future__ import annotations

from typing import overload, Dict, List

from .errors import JsonLoadError
from .json_core import JsonSchema, Keyword
from .uri import Uri
from .uri_loader import DefaultLoader, UriLoader

__all__ = ["JsonStore"]


class JsonStore:
    _instance: JsonStore = None

    def __init__(self):
        self._storage: Dict[str, JsonSchema] = {}
        self.loader: UriLoader = DefaultLoader()

    def add(self, uri: Uri, document: JsonSchema) -> None:
        if not uri.is_absolute:
            raise ValueError(f"JsonStore.add `uri` parameter must be an absolute uri, `{uri}` given instead.")
        self._storage[str(uri.base_uri)] = document

    @overload
    def get(self, uri: str) -> JsonSchema:
        ...

    @overload
    def get(self, uri: Uri) -> JsonSchema:
        ...

    def get(self, uri) -> JsonSchema:
        if isinstance(uri, str):
            return self._storage[uri]
        if isinstance(uri, Uri):
            return self._storage[str(uri.base_uri)]

        raise TypeError(f"JsonStore.get expects uri to be `str` or `Uri`, `{type(uri)}` given instead.")

    @overload
    def __contains__(self, key: Uri) -> bool:
        ...

    @overload
    def __contains__(self, key: str) -> bool:
        ...

    def __contains__(self, key) -> bool:
        if isinstance(key, str):
            return key in self._storage
        if isinstance(key, Uri):
            return str(key.base_uri) in self._storage

        raise TypeError(
            f"JsonStore.__contains__ expects `key` argument to be one of: `JsonUri`, `str`, `{type(key)}` given."
        )

    @overload
    def load(self, uri: Uri, vocabulary: List[Keyword] = None) -> JsonSchema:
        ...

    @overload
    def load(self, file: str, vocabulary: List[Keyword] = None) -> JsonSchema:
        ...

    def load(self, obj, vocabulary: List[Keyword] = None) -> JsonSchema:
        if vocabulary is None:
            vocabulary = []

        if isinstance(obj, Uri):
            return self.load_uri(obj, vocabulary)
        if isinstance(obj, str):
            return self.load_uri(Uri(obj), vocabulary)

        raise TypeError(
            f"JsonStore.load() expects `obj` argument to be one of: `JsonUri`, `str`, `{type(obj)}` given."
        )

    def load_uri(self, uri: Uri, vocabulary: List[Keyword]) -> JsonSchema:
        base_uri = str(uri.base_uri)
        if base_uri in self._storage:
            return self._storage[base_uri]

        try:
            document = self.loader.load(uri, vocabulary)
            self._storage[base_uri] = document
            return document
        except FileNotFoundError as e:
            raise JsonLoadError.for_invalid_file(uri, e.filename) from e

    @classmethod
    def default(cls) -> JsonStore:
        if cls._instance is None:
            cls._instance = cls()
            return cls._instance

        return cls._instance
