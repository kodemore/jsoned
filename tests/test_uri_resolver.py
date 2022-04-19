from os import path

import pytest

from jsoned import UriResolver, Uri, MappableUriResolver


def test_can_instantiate() -> None:
    # given
    resolver = MappableUriResolver()

    # then
    assert isinstance(resolver, UriResolver)


def test_resolve_mapped_path() -> None:
    # given
    resolver = MappableUriResolver()
    test_uri = Uri("https://test.com/schemes/schema_plain.json")
    dir_name = path.dirname(__file__)

    # when
    resolver.map("https://test.com/schemes/", path.join(dir_name, "fixtures"))

    # then
    assert resolver.resolve(test_uri) == path.join(
        dir_name, "fixtures", "schema_plain.json"
    )


def test_fail_to_resolve() -> None:
    # given
    resolver = MappableUriResolver()
    test_uri = Uri("https://test.com/schemes/local_schema.json")

    with pytest.raises(ValueError):
        resolver.resolve(test_uri)
