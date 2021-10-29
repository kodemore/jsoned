from jsoned import JsonUriResolver, JsonUri
from os import path


def test_can_instantiate() -> None:
    # given
    resolver = JsonUriResolver()

    # then
    assert isinstance(resolver, JsonUriResolver)


def test_resolve_mapped_path() -> None:
    # given
    resolver = JsonUriResolver()
    sample_uri = JsonUri("https://mydomain.com/schemes/local_schema.json")
    dir_name = path.dirname(__file__)

    # when
    resolver.map("https://mydomain.com/schemes/", path.join(dir_name, "fixtures"))

    # then
    assert resolver.resolve(sample_uri) == path.join(dir_name, "fixtures", "local_schema.json")
