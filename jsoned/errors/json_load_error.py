from __future__ import annotations

from jsoned.uri import Uri

__all__ = ["JsonLoadError"]


class JsonLoadError(RuntimeError):
    @classmethod
    def for_incomplete_uri(cls, uri: Uri) -> JsonLoadError:
        return cls(
            f"Could not load document from given uri {uri}, scheme and/or path is missing."
            f"Declare `id` or `$id` property in your json document and retry."
        )
