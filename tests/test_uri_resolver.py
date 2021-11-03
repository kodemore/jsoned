import pytest

from jsoned import UriResolver, Uri
from os import path

from jsoned.uri_resolver import CustomResolver


def test_can_instantiate() -> None:
    # given
    resolver = UriResolver()

    # then
    assert isinstance(resolver, UriResolver)


def test_resolve_mapped_path() -> None:
    # given
    resolver = UriResolver()
    test_uri = Uri("https://test.com/schemes/schema_plain.json")
    dir_name = path.dirname(__file__)

    # when
    resolver.map("https://test.com/schemes/", path.join(dir_name, "fixtures"))

    # then
    assert resolver.resolve(test_uri) == path.join(dir_name, "fixtures", "schema_plain.json")


def test_use_custom_resolver_for_scheme() -> None:
    # given
    resolver = UriResolver()
    test_uri = Uri("https://test.com/schemes/schema_plain.json")

    class MyResolver(CustomResolver):
        def resolve(self, uri: Uri) -> str:
            return path.join(path.sep, "etc", *uri.path.split("/"))

    # when
    resolver.register("https", MyResolver())

    # then
    assert resolver.resolve(test_uri) == path.join(path.sep, "etc", "schemes", "schema_plain.json")


def test_fail_to_resolve() -> None:
    # given
    resolver = UriResolver()
    test_uri = Uri("https://test.com/schemes/local_schema.json")

    with pytest.raises(ValueError):
        resolver.resolve(test_uri)
