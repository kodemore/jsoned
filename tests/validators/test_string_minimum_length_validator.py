import pytest

from jsoned.errors import MinimumValidationError, MinimumLengthValidationError
from jsoned.validators.string_validators import StringMinimumLengthValidator


def test_can_instantiate() -> None:
    # given
    instance = StringMinimumLengthValidator(10)

    # then
    assert isinstance(instance, StringMinimumLengthValidator)


def test_pass_validation() -> None:
    # given
    instance = StringMinimumLengthValidator(3)

    # then
    instance("abc")


def test_fail_validation() -> None:
    # given
    instance = StringMinimumLengthValidator(10)

    # then
    with pytest.raises(MinimumLengthValidationError):
        instance("abc")
