from __future__ import annotations

from rfc3986 import URIReference



class Uri:
    def __init__(self, uri: str) -> None:
        self._value = URIReference.from_string(uri)
        if self._value.scheme:
            self._value = self._value.normalize()

    def __str__(self) -> str:
        return self._value.unsplit()

    def __repr__(self) -> str:
        return f"Uri({str(self)!r})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Uri):
            return self._value == other._value
        if other is None:
            return False
        return self._value.__eq__(other)

    @property
    def scheme(self) -> str:
        return self._value.scheme

    @property
    def authority(self) -> str:
        return self._value.authority

    @property
    def path(self) -> str:
        return self._value.path

    @property
    def query(self) -> str:
        return self._value.query

    @property
    def fragment(self) -> str:
        return self._value.fragment

    def __bool__(self) -> bool:
        return self.scheme is not None or \
               self.authority is not None or \
               self.path is not None or \
               self.query is not None or \
               self.fragment is not None

    @property
    def base_uri(self) -> Uri:
        uri = Uri.__new__(Uri)
        uri._value = self._value.copy_with(fragment=None)

        return uri

    def is_absolute(self) -> bool:
        return self._value.is_absolute()

    def resolve(self, other: Uri) -> Uri:
        uri = Uri.__new__(Uri)
        uri._value = other.base_uri._value

        uri._value = uri._value.resolve_with(self.base_uri._value)

        if other.fragment:
            uri._value = uri._value.copy_with(fragment=other.fragment)

        return uri
