from __future__ import annotations

from jsoned.json_uri import JsonUri

__all__ = ["JsonLoadError"]


class JsonLoadError(RuntimeError):

    @classmethod
    def for_incomplete_uri(cls, uri: JsonUri) -> JsonLoadError:
        return cls(f"Could not load document from given uri {uri}, scheme and/or path is missing."
                   f"Declare `id` or `$id` property in your json document and retry.")
