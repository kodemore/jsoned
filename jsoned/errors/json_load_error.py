from __future__ import annotations

from jsoned.uri import Uri

__all__ = ["JsonLoadError"]


class JsonLoadError(RuntimeError):
    uri: Uri

    @classmethod
    def for_incomplete_uri(cls, uri: Uri) -> JsonLoadError:
        instance = cls(
            f"Could not load document from given uri `{uri}`, scheme and/or path is missing. "
            f"Declare `id` or `$id` property in your json document and retry."
        )
        instance.uri = uri

        return instance

    @classmethod
    def for_invalid_file(cls, uri: Uri, filename: str) -> JsonLoadError:
        instance = cls(
            f"Could not load document from given uri `{uri}`. "
            f"Corresponding file `{filename}` does not exists"
        )
        instance.uri = uri

        return instance
