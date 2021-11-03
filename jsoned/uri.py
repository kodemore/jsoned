from __future__ import annotations

from typing import overload

from rfc3986 import misc
from rfc3986.normalizers import (
    normalize_scheme,
    normalize_path,
    normalize_fragment,
    normalize_query,
)


class Authority:
    def __init__(self, authority: str):
        matched = misc.SUBAUTHORITY_MATCHER.match(authority).groupdict()
        self._userinfo = matched["userinfo"] or ""
        self._host = matched["host"] or ""
        self._port = matched["port"] or ""

    @property
    def userinfo(self) -> str:
        return self._userinfo

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> str:
        return self._port

    def __str__(self):
        result = []
        if self.userinfo:
            result.append(f"{self.userinfo}@")
        if self.host:
            result.append(self.host)
        if self.port:
            result.append(f":{self.port}")

        return "".join(result)

    def __bool__(self) -> bool:
        return self.userinfo != "" or self.host != "" or self.port != ""

    def __repr__(self) -> str:
        return f"Authority({str(self)!r})"


class Uri:
    def __init__(self, uri: str) -> None:
        matched = misc.URI_MATCHER.match(uri).groupdict()

        self._scheme = normalize_scheme(matched["scheme"] or "")
        self._authority = Authority(matched["authority"] or "")
        self._query = normalize_query(matched["query"] or "")
        self._fragment = normalize_fragment(matched["fragment"] or "")

        if self._scheme:
            self._path = normalize_path(matched["path"] or "")
        else:
            self._path = matched["path"] or ""

    @property
    def scheme(self) -> str:
        return self._scheme

    @property
    def authority(self) -> Authority:
        return self._authority

    @property
    def path(self) -> str:
        return self._path

    @property
    def query(self) -> str:
        return self._query

    @property
    def fragment(self) -> str:
        return self._fragment

    @property
    def base_uri(self) -> Uri:
        return self.copy_with(fragment="", query="")

    @property
    def is_absolute(self) -> bool:
        str_uri = str(self.copy_with(query="", fragment=""))
        return bool(misc.ABSOLUTE_URI_MATCHER.match(str_uri))

    @property
    def host(self) -> str:
        return self._authority.host

    @property
    def port(self) -> str:
        return self._authority.port

    @overload
    def resolve(self, uri: str) -> Uri:
        ...

    @overload
    def resolve(self, uri: Uri) -> Uri:
        ...

    def resolve(self, uri) -> Uri:
        if isinstance(uri, str):
            uri = Uri(uri)

        if isinstance(uri, Uri):
            if uri.is_absolute:  # for absolute uris there is nothing to resolve
                return uri.copy_with()

            if uri.path == "":
                return self.copy_with(
                    query=uri.query if uri.query else None, fragment=uri.fragment
                )
            elif uri.path.startswith("/"):
                return self.copy_with(
                    query=uri.query, fragment=uri.fragment, path=uri.path
                )

            path = self.path
            index = path.rfind("/")
            path = path[:index] + "/" + uri.path
            result = self.copy_with(query=uri.query, fragment=uri.fragment, path=path)

            return result

        raise TypeError(
            "Uri.resolve expects parameter to be instance of `str` or `Uri`"
        )

    def copy_with(
        self,
        scheme: str = None,
        authority: str = None,
        path: str = None,
        query: str = None,
        fragment: str = None,
    ) -> Uri:
        instance = Uri.__new__(Uri)
        instance._scheme = (
            normalize_scheme(scheme) if scheme is not None else self._scheme
        )
        instance._authority = (
            Authority(authority) if authority is not None else self._authority
        )
        instance._path = path if path is not None else self._path
        instance._query = normalize_query(query) if query is not None else self._query
        instance._fragment = (
            normalize_fragment(fragment) if fragment is not None else self._fragment
        )

        if instance.scheme:
            instance._path = normalize_path(instance._path)

        return instance

    def __str__(self) -> str:
        result = []
        if self.scheme:
            result.append(f"{self.scheme}://")
        if self.authority:
            result.append(f"{self.authority}")
        if self.path:
            result.append(self.path)
        if self.query:
            result.append(f"?{self.query}")
        if self.fragment:
            result.append(f"#{self.fragment}")
        return "".join(result)

    def __repr__(self) -> str:
        return f"Uri({str(self)!r})"

    def __hash__(self) -> int:
        return hash(repr(self))

    @overload
    def __eq__(self, other: str) -> bool:
        ...

    @overload
    def __eq__(self, other: Uri) -> bool:
        ...

    def __eq__(self, other) -> bool:
        if isinstance(other, Uri):
            return (
                self.scheme == other.scheme
                and self.authority == other.authority
                and self.path == other.path
                and self.query == other.query
                and self.fragment == other.fragment
            )

        if isinstance(other, str):
            other_uri = Uri(other)

            return self == other_uri

        raise TypeError(
            f"Uri.__eq__ expects value to be `str` or `Uri`, `{type(other)}` passed instead."
        )

    def __bool__(self) -> bool:
        return (
            self.scheme != ""
            or bool(self.authority)
            or self.path != ""
            or self.query != ""
            or self.fragment != ""
        )
