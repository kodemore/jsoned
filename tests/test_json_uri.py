import pytest

from jsoned import JsonUri


def test_can_instantiate() -> None:
    assert JsonUri("https://test.com/test")


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
    uri = JsonUri(uri_str)

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
    uri = JsonUri(uri_str)

    # then
    assert uri.fragment == expected


@pytest.mark.parametrize(
    "uri_str,expected",
    [
        ["file://path/to/file.json#fragment/part", "/path/to/file.json"],
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
    uri = JsonUri(uri_str)

    # then
    assert uri.path == expected


@pytest.mark.parametrize(
    "uri_str,expected",
    [
        ["file://path/to/file.json#fragment/part", ""],
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
    uri = JsonUri(uri_str)

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
    uri = JsonUri(uri_str)

    # then
    assert uri.is_absolute is expected


@pytest.mark.parametrize(
    "uri_str,expected",
    [
        ["file://path/to/file.json#fragment/part", False],
        ["https://path/to/file.json#fragment/part", False],
        ["https://path/to/file.json?q=1#fragment/part", False],
        ["https://path/to/file.json", False],
        ["https://path/to/file.json?q=1", False],
        ["#fragment/part", True],
        ["path/to/file.json#fragment/part", True],
        ["/path/to/file.json?q=1#fragment/part", False],
        ["../path/to/file.json", True],
        ["./path/to/file.json?q=1", True],
    ],
)
def test_is_relative(uri_str: str, expected: bool) -> None:
    # when
    uri = JsonUri(uri_str)

    # then
    assert uri.is_relative is expected


@pytest.mark.parametrize(
    "base,other,expected",
    [
        [
            "file://path/to/file.json#fragment/part",
            "file://other/path/to/file.json#fragment/part",
            "file://other/path/to/file.json#fragment/part",
        ],
        [
            "file://path/to/file.json#fragment/part",
            "../other.json",
            "file://path/other.json",
        ],
        [
            "file://path/to/file.json#fragment/part",
            "/path/to/file.json#fragment/part2",
            "file://path/to/file.json#fragment/part2",
        ],
        [
            "file://path/to/file.json#fragment/part",
            "#fragment-2",
            "file://path/to/file.json#fragment-2",
        ],
        [
            "file://path/to/file.json#fragment/part",
            "./to/file.json",
            "file://path/to/to/file.json",
        ],
        [
            "file://path/to/file.json#fragment/part",
            "/to/file.json",
            "file://to/file.json",
        ],
        ["path/to/file.json#fragment/part", "to/file.json", "path/to/to/file.json"],
    ],
)
def test_can_add_two_uris(base: str, other: str, expected: str) -> None:
    # given
    base_uri = JsonUri(base)
    other_uri = JsonUri(other)

    # when
    result = base_uri + other_uri
    result_str = base_uri + other

    # then
    assert isinstance(result, JsonUri)
    assert isinstance(result_str, JsonUri)
    assert str(result) == expected
    assert str(result_str) == expected


def test_can_contain_only_fragment() -> None:
    # given
    uri = JsonUri("#/only/fragment")

    # then
    assert not uri.base_uri
    assert uri.fragment == "/only/fragment"
