import pytest

from jsoned import Uri


def test_can_instantiate() -> None:
    assert Uri("https://test.com/test")


@pytest.mark.parametrize(
    "uri_str,expected",
    [
        ["file://path/to/file.json#fragment/part", "file"],
        ["https://path/to/file.json#fragment/part", "https"],
        ["https://path/to/file.json?q=1#fragment/part", "https"],
        ["/path/to/file.json#fragment/part", ""],
        ["path/to/file.json", ""],
        ["./to/file.json", ""],
        ["#fragment/part", ""],
    ],
)
def test_can_get_scheme(uri_str: str, expected: str) -> None:
    # when
    uri = Uri(uri_str)

    # then
    assert uri.scheme == expected


@pytest.mark.parametrize(
    "uri_str,expected",
    [
        ["file://path/to/file.json#fragment/part", "fragment/part"],
        ["https://path/to/file.json#fragment/part", "fragment/part"],
        ["https://path/to/file.json?q=1#fragment/part", "fragment/part"],
        ["/path/to/file.json#fragment/part", "fragment/part"],
        ["path/to/file.json", ""],
        ["./to/file.json", ""],
        ["#fragment/part", "fragment/part"],
    ],
)
def test_can_get_fragment(uri_str: str, expected: str) -> None:
    # when
    uri = Uri(uri_str)

    # then
    assert uri.fragment == expected


@pytest.mark.parametrize(
    "uri_str,expected",
    [
        ["http://domain.com/to/file.json#fragment/part", "/to/file.json"],
        ["https://path/to/file.json#fragment/part", "/to/file.json"],
        ["https://path/to/file.json?q=1#fragment/part", "/to/file.json"],
        ["/path/to/file.json#fragment/part", "/path/to/file.json"],
        ["path/to/file.json", "path/to/file.json"],
        ["./to/file.json", "./to/file.json"],
        ["#fragment/part", ""],
    ],
)
def test_can_get_path(uri_str: str, expected: str) -> None:
    # when
    uri = Uri(uri_str)

    # then
    assert uri.path == expected


@pytest.mark.parametrize(
    "uri_str,expected",
    [
        ["http://test.com/to/file.json#fragment/part", "test.com"],
        ["https://path/to/file.json#fragment/part", "path"],
        ["https://path/to/file.json?q=1#fragment/part", "path"],
        ["/path/to/file.json#fragment/part", ""],
        ["path/to/file.json", ""],
        ["./to/file.json", ""],
        ["#fragment/part", ""],
    ],
)
def test_can_get_host(uri_str: str, expected: str) -> None:
    # when
    uri = Uri(uri_str)

    # then
    assert uri.host == expected


@pytest.mark.parametrize(
    "uri_str,expected",
    [
        ["file://path/to/file.json#fragment/part", True],
        ["https://path/to/file.json#fragment/part", True],
        ["https://path/to/file.json?q=1#fragment/part", True],
        ["https://path/to/file.json", True],
        ["https://path/to/file.json?q=1", True],
        ["#fragment/part", False],
        ["path/to/file.json#fragment/part", False],
        ["/path/to/file.json?q=1#fragment/part", False],
        ["../path/to/file.json", False],
        ["./path/to/file.json?q=1", False],
    ],
)
def test_is_absolute(uri_str: str, expected: bool) -> None:
    # when
    uri = Uri(uri_str)

    # then
    assert uri.is_absolute is expected


@pytest.mark.parametrize(
    "base,other,expected",
    [
        [
            "http://test.com/path/to/file.json",
            "../some/file.json",
            "http://test.com/path/some/file.json"
        ],
        [
            "http://test.com/to/file.json#fragment/part",
            "http://test.com/path/to/file.json#fragment/part",
            "http://test.com/path/to/file.json#fragment/part",
        ],
        [
            "http://test.com/to/file.json#fragment/part",
            "../other.json",
            "http://test.com/other.json",
        ],
        [
            "http://test.com/to/file.json#fragment/part",
            "/path/to/file.json#fragment/part2",
            "http://test.com/path/to/file.json#fragment/part2",
        ],
        [
            "http://test.com/to/file.json#fragment/part",
            "#fragment-2",
            "http://test.com/to/file.json#fragment-2",
        ],
        [
            "http://test.com/to/file.json#fragment/part",
            "./to/file.json",
            "http://test.com/to/to/file.json",
        ],
        [
            "http://test.com/to/file.json#fragment/part",
            "to/file.json",
            "http://test.com/to/to/file.json",
        ],
    ],
)
def test_can_resolve_relative_uris(base: str, other: str, expected: str) -> None:
    # given
    base_uri = Uri(base)
    other_uri = Uri(other)

    # when
    result = base_uri.resolve(other_uri)

    # then
    assert isinstance(result, Uri)
    assert str(result) == expected


def test_can_contain_only_fragment() -> None:
    # given
    uri = Uri("#/only/fragment")

    # then
    assert not uri.base_uri
    assert uri.fragment == "/only/fragment"


def test_can_normalise_uri() -> None:
    # given
    uri_str = "https://domain.com/../some/../path/index.htm"

    # when
    uri = Uri(uri_str)

    # then
    assert str(uri) == "https://domain.com/path/index.htm"
