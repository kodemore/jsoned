from jsoned.types import JsonArray, JsonType


def test_can_instantiate() -> None:
    # given
    instance = JsonArray([])

    # then
    assert isinstance(instance, JsonArray)


def test_can_get_item() -> None:
    # given
    instance = JsonArray([1])

    # when
    item = instance[0]

    # then
    assert isinstance(item, JsonType)
    assert item.key == "0"


def test_can_use_len() -> None:
    # given
    instance = JsonArray([1, 2, 3])

    # then
    assert len(instance) == 3


def test_set_item() -> None:
    # given
    instance = JsonArray([1, 2, 3])

    # when
    assert instance[1] == 2
    instance[1] = 5

    # then
    assert instance[1] == 5


def test_compare_with_list() -> None:
    assert JsonArray([1]) == [1]
    assert JsonArray([2, True, 5, 1.0]) == [2, True, 5, 1.0]


def test_can_get_slice() -> None:
    # given
    instance = JsonArray([1, 2, 3])

    # when
    slice = instance[0:2]

    # then
    assert slice == [1, 2]


def test_can_delete_item() -> None:
    # given
    instance = JsonArray([1, 2, 3])

    # when
    del instance[0]

    # then
    assert instance == [2, 3]


def test_can_use_in() -> None:
    # given
    instance = JsonArray(["a", 1, 2.3])

    # then
    assert 1 in instance
    assert False not in instance
    assert "a" in instance
