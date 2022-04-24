import pytest

from jsoned.errors import EnumValidationError
from jsoned.validators import EnumValidator


def test_can_instantiate() -> None:
    # given
    instance = EnumValidator(["object"])

    # then
    assert isinstance(instance, EnumValidator)


def test_pass_validation() -> None:
    # given
    instance = EnumValidator(["object", "string", 1, False])

    # then
    instance("object")
    instance("string")
    instance(1)
    instance(False)


def test_fail_validation() -> None:
    # given
    instance = EnumValidator(["object", "string", 1, False])

    # then
    # then
    with pytest.raises(EnumValidationError) as e:
        instance("a")

    error = e.value
    assert error.code == "enum_error"
    assert error.path == ""
    assert error.expected_values == ["object", "string", 1, False]
