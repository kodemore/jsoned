import re

from copy import copy

from typing import Union

__all__ = ["JsonUri"]

SCHEME_REGEX = "[a-zA-Z][a-zA-Z0-9+.-]*"
HOST_REGEX = "[^\\\\/?#]*"
PATH_REGEX = "[^?#]*"
QUERY_REGEX = "[^#]*"
FRAGMENT_REGEX = ".*"
URI_PARTS = {
    "scheme": SCHEME_REGEX,
    "host": HOST_REGEX,
    "path": PATH_REGEX,
    "query": QUERY_REGEX,
    "fragment": FRAGMENT_REGEX,
}
URI_REGEX = (
    r"(?:(?P<scheme>{scheme}):)?(?://(?P<host>{host})?)?"
    r"(?P<path>{path})(?:\?(?P<query>{query}))?"
    r"(?:#(?P<fragment>{fragment}))?"
).format(**URI_PARTS)
URI_MATCHER = re.compile(URI_REGEX)
JSON_SCHEMA_FILE_EXTENSIONS = ["json", "jsd", "jsonsd", "yml", "yaml"]


class JsonUri:
    def __init__(self, uri: str):
        matched = URI_MATCHER.match(uri.lower())
        if not matched:
            raise ValueError(f"Passed string `{uri}` is not a valid uri.")

        self._scheme = matched.group("scheme") if matched.group("scheme") else ""
        self._host = matched.group("host") if matched.group("host") else ""
        self._path = matched.group("path") if matched.group("path") else ""
        self._query = matched.group("query") if matched.group("query") else ""
        self._fragment = matched.group("fragment") if matched.group("fragment") else ""

        if self._is_local_scheme:
            self._path = self._host + self._path
            self._host = ""
            self._query = ""

        if self._scheme:
            self._path = normalise_path(self._path)

    def __repr__(self):
        return f"JsonUri({self})"

    @property
    def base_uri(self) -> str:
        if self._is_local_scheme:
            result = f"{self._scheme}://"
            result += self._path[1:] if self._path[0] == "/" else self._path

        elif self.scheme:
            result = f"{self._scheme}://{self._host}{self._path}"
        else:
            result = f"{self._host}{self._path}"

        return result

    def __str__(self):
        result = self.base_uri

        if self._query:
            result += f"?{self._query}"
        if self._fragment:
            result += f"#{self._fragment}"

        return result

    @property
    def scheme(self) -> str:
        return self._scheme

    @property
    def path(self) -> str:
        # normalise paths for absolute uris
        if self._scheme and self._path[0] != "/":
            return "/" + self._path

        return self._path

    @property
    def fragment(self) -> str:
        return self._fragment

    @property
    def host(self) -> str:
        return self._host

    @property
    def query(self) -> str:
        return self._query

    @property
    def is_absolute(self) -> bool:
        return self.scheme != "" and (self.host != "" or self.path != "")

    @property
    def _is_local_scheme(self) -> bool:
        return self.scheme == "file" or self.scheme == "memory"

    @property
    def is_relative(self) -> bool:
        return not self.scheme and (not self.path or self.path[0] != "/")

    def __copy__(self) -> "JsonUri":
        result = JsonUri.__new__(JsonUri)
        result._scheme = self._scheme
        result._host = self._host
        result._path = self._path
        result._query = self._query
        result._fragment = self._fragment

        return result

    def resolve(self, other: Union[str, "JsonUri"]) -> "JsonUri":
        result = copy(self)

        if not isinstance(other, JsonUri):
            other = JsonUri(other)

        if other.is_absolute:
            return copy(other)

        if not other.is_relative:
            result._path = other._path
            result._query = other._query
            result._fragment = other._fragment
            return result

        if self.path == other.path:
            result._query = other._query
            result._fragment = other._fragment
            return result

        if not other.path:
            result._query = other._query if other._query else self._query
            result._fragment = other._fragment
            return result

        result._fragment = other._fragment
        result._host = ""

        current_path = self.path.split("/")
        new_path = other.path.split("/")

        # remove last item if it is a json schema file
        if current_path[-1].split(".")[-1] in JSON_SCHEMA_FILE_EXTENSIONS:
            current_path.pop()

        for item in new_path:
            if item == "..":
                current_path.pop()
                continue
            if item == ".":
                continue
            current_path.append(item)

        result._path = "/".join(current_path)

        return result
