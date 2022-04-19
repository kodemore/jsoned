from __future__ import annotations

from abc import abstractmethod
from os import path
from typing import Protocol, runtime_checkable

from .uri import Uri

__all__ = ["UriResolver", "MappableUriResolver"]


@runtime_checkable
class UriResolver(Protocol):
    @abstractmethod
    def resolve(self, uri: Uri) -> str:
        ...


class MappableUriResolver(UriResolver):
    def __init__(self):
        self._map = {}

    def map(self, uri: str, target_path: str) -> None:
        self._map[uri] = target_path

    def resolve(self, uri: Uri) -> str:
        uri_str = str(uri.base_uri)
        resolved_path = ""
        resolved_uri = ""
        for mapping_uri, mapped_path in self._map.items():
            if not uri_str.startswith(mapping_uri):
                continue
            resolved_path = mapped_path
            resolved_uri = mapping_uri
            break

        if resolved_path:
            remaining_path = uri_str[len(resolved_uri):].split("/")

            return path.join(resolved_path, *remaining_path)

        if not uri.scheme or uri.scheme == "file":
            return uri.path

        raise ValueError(
            f"Could not resolve {uri} to any path. Either scheme is unsupported or there is no mapping set for the uri."
            f"You can try to add your path to mapping by calling `{self.__class__}.map` function."
        )
