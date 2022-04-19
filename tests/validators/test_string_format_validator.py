import pytest

from jsoned.errors import FormatValidationError
from jsoned.validators.string_validators import StringFormatValidator


def test_can_instantiate() -> None:
    # given
    instance = StringFormatValidator("email")

    # then
    assert isinstance(instance, StringFormatValidator)


def test_pass_validation() -> None:
    # given
    instance = StringFormatValidator("email")

    # then
    instance("test@test.com")
    instance("abc@gmail.com")


def test_fail_validation() -> None:
    # given
    instance = StringFormatValidator("email")

    # then
    with pytest.raises(FormatValidationError):
        instance("abc")
