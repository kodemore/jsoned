import pytest
from tests.fixtures import jsonpointer_fixture
from hypothesis import given

from jsoned import JsonPointer


@given(jsonpointer_fixture)
def test_can_instantiate(pointer_str: str) -> None:
    # when
    pointer = JsonPointer(pointer_str)

    # then
    assert str(pointer) == pointer_str
