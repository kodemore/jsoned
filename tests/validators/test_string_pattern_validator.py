import pytest

from jsoned.errors import FormatValidationError
from jsoned.validators.string_validators import StringPatternValidator


def test_can_instantiate() -> None:
    # given
    instance = StringPatternValidator("email")

    # then
    assert isinstance(instance, StringPatternValidator)


def test_pass_validation() -> None:
    # given
    instance = StringPatternValidator("[a-z]+")

    # then
    instance("abcd")
    instance("edfgkaoe")


def test_fail_validation() -> None:
    # given
    instance = StringPatternValidator("[a-z]+")

    # then
    with pytest.raises(FormatValidationError):
        instance("@")
