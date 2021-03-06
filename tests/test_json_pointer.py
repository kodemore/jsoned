from hypothesis import given

from jsoned import JsonPointer
from tests.fixtures import jsonpointer_fixture


@given(jsonpointer_fixture)
def test_can_instantiate(pointer_str: str) -> None:
    # when
    pointer = JsonPointer(pointer_str)

    # then
    if pointer_str == "":
        assert str(pointer) == "/"
    else:
        assert str(pointer) == pointer_str
