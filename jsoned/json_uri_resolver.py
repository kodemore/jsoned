from __future__ import annotations

from typing import Callable, Any

from jsoned.json_uri import JsonUri

__all__ = ["JsonUriResolver"]


CustomResolver = Callable[[JsonUri], str]


class JsonUriResolver:
    """
    Resolves passed JsonUri to local filename.
    """

    def __init__(self):
        ...

    def map(self, uri: str, path: str) -> None:
        ...

    def register(self, scheme: str, resolver: CustomResolver) -> None:
        ...

    def resolve(self, uri: JsonUri) -> Any:
        ...
