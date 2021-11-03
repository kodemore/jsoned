from __future__ import annotations

from abc import abstractmethod
from functools import lru_cache
from os import path
from typing import Protocol

from .uri import Uri

__all__ = ["UriResolver", "CustomResolver"]


class CustomResolver(Protocol):

    @abstractmethod
    def resolve(self, uri: Uri) -> str:
        ...


class UriResolver(CustomResolver):
    """
    Resolves passed Uri to local filename.
    """

    def __init__(self):
        self._map = {}
        self._scheme_resolvers = {}

    def map(self, uri: str, target_path: str) -> None:
        self._map[uri] = target_path

    def register(self, scheme: str, resolver: CustomResolver) -> None:
        self._scheme_resolvers[scheme] = resolver

    @lru_cache
    def resolve(self, uri: Uri) -> str:
        if uri.scheme in self._scheme_resolvers:
            return self._scheme_resolvers[uri.scheme].resolve(uri)

        uri_str = str(uri.base_uri)
        resolved_path = ""
        resolved_uri = ""
        for mapping_uri, mapped_path in self._map.items():
            if not uri_str.startswith(mapping_uri):
                continue
            resolved_path = mapped_path
            resolved_uri = mapping_uri
            break

        if not resolved_path:
            raise ValueError(
                f"Could not resolve {uri} to any path. "
                f"Please try to add your path to mapping by calling `UriResolver.map` function."
            )
        remaining_path = uri_str[len(resolved_uri):].split("/")

        return path.join(resolved_path, *remaining_path)
