import pytest

from jsoned.errors import EnumValidationError, ConstValidationError
from jsoned.validators import ConstValidator


def test_can_instantiate() -> None:
    # given
    instance = ConstValidator(["object"])

    # then
    assert isinstance(instance, ConstValidator)


def test_pass_validation() -> None:
    # given
    instance = ConstValidator("test")

    # then
    instance("test")


def test_fail_validation() -> None:
    # given
    instance = ConstValidator("test")

    # then
    # then
    with pytest.raises(ConstValidationError) as e:
        instance("a")

    error = e.value
    assert error.code == "const_error"
    assert error.path == ""
    assert error.expected_value == "test"
