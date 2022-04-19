from __future__ import annotations

from abc import abstractmethod, ABC
from decimal import Decimal
from functools import lru_cache, partial
from json import load as _load_json
from os import path

from yaml import FullLoader as YamlFullLoader, load as _load_yaml

from jsoned.json_core import JsonSchema, Vocabulary
from .uri import Uri
from .uri_resolver import UriResolver

load_yaml = partial(_load_yaml, Loader=YamlFullLoader)
load_json = partial(_load_json, parse_float=Decimal)

_SUPPORTED_FORMATS = {
    ".yaml": load_yaml,
    ".yml": load_yaml,
    ".json": load_json,
}


__all__ = ["DefaultLoader", "UriLoader"]


class UriLoader(ABC):
    @abstractmethod
    def load(self, uri: Uri, vocabulary: Vocabulary = None) -> JsonSchema:
        ...

    @abstractmethod
    def register(self, scheme: str, resolver: UriResolver) -> None:
        ...


class DefaultLoader(UriResolver, UriLoader):
    """
    Resolves passed Uri to local filename.
    """

    def __init__(self):
        self._scheme_resolvers = {}

    def register(self, scheme: str, resolver: UriResolver) -> None:
        self._scheme_resolvers[scheme] = resolver

    @lru_cache()
    def resolve(self, uri: Uri) -> str:
        if uri.scheme in self._scheme_resolvers:
            resolver = self._scheme_resolvers[uri.scheme]
            return resolver.resolve(uri)

        if not uri.scheme or uri.scheme == "file":
            return uri.path

        raise ValueError(
            f"Could not resolve `{uri}` to any path. "
            f"Unsupported scheme `{uri.scheme}`."
        )

    def load(self, uri: Uri, vocabulary: Vocabulary = None) -> JsonSchema:
        filename = self.resolve(uri)

        return self.load_file(filename, vocabulary)

    @staticmethod
    def load_file(filename: str, vocabulary: Vocabulary) -> JsonSchema:
        file = open(filename, "r")
        _, extension = path.splitext(file.name)
        if extension not in _SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported file format `{extension}`, expected `json` or `yaml`.")

        json = _SUPPORTED_FORMATS[extension](file)

        return JsonSchema(json, vocabulary)
