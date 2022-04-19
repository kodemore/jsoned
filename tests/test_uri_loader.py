from os import path

from jsoned import DefaultLoader, Uri, UriResolver, UriLoader


def test_can_instantiate() -> None:
    # given
    instance = DefaultLoader()

    # then
    assert isinstance(instance, DefaultLoader)
    assert isinstance(instance, UriResolver)
    assert isinstance(instance, UriLoader)


def test_can_use_custom_resolver_for_scheme() -> None:
    # given
    resolver = DefaultLoader()
    test_uri = Uri("https://test.com/schemes/schema_plain.json")

    class MyResolver(UriResolver):
        def resolve(self, uri: Uri) -> str:
            return path.join(path.sep, "etc", *uri.path.split("/"))

    # when
    resolver.register("https", MyResolver())

    # then
    assert resolver.resolve(test_uri) == path.join(
        path.sep, "etc", "schemes", "schema_plain.json"
    )
