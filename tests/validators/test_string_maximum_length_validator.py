import pytest

from jsoned.errors import MaximumLengthValidationError
from jsoned.validators.string_validators import StringMaximumLengthValidator


def test_can_instantiate() -> None:
    # given
    instance = StringMaximumLengthValidator(10)

    # then
    assert isinstance(instance, StringMaximumLengthValidator)


def test_pass_validation() -> None:
    # given
    instance = StringMaximumLengthValidator(3)

    # then
    instance("abc")
    instance("bc")


def test_fail_validation() -> None:
    # given
    instance = StringMaximumLengthValidator(2)

    # then
    with pytest.raises(MaximumLengthValidationError):
        instance("abc")
