import pytest

from jsoned.errors import TypeValidationError
from jsoned.validators import TypeValidator


def test_can_instantiate() -> None:
    # given
    instance = TypeValidator(["object"])

    # then
    assert isinstance(instance, TypeValidator)


def test_pass_validation() -> None:
    # given
    instance = TypeValidator(["object", "string"])

    # then
    instance({})
    instance({"a": 1})
    instance("aa")


def test_fail_validation() -> None:
    # given
    instance = TypeValidator(["object", "string"])

    # then
    with pytest.raises(TypeValidationError) as e:
        instance(True)

    error = e.value
    assert error.code == "type_error"
    assert error.path == ""
    assert error.expected_types == ["object", "string"]
