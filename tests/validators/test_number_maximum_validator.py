from decimal import Decimal

import pytest

from jsoned.errors import MaximumValidationError
from jsoned.validators.number_validators import NumberMaximumValidator


def test_can_instantiate() -> None:
    # given
    instance = NumberMaximumValidator(Decimal("10"))

    # then
    assert isinstance(instance, NumberMaximumValidator)


def test_pass_validation() -> None:
    # given
    instance = NumberMaximumValidator(Decimal("10"))

    # then
    instance(10)
    instance(9)


def test_pass_validation_with_exclusive_flag() -> None:
    # given
    instance = NumberMaximumValidator(Decimal("10"), exclusive=True)

    # then
    instance(9)
    instance(8)


def test_fail_validation() -> None:
    # given
    instance = NumberMaximumValidator(Decimal("10"))

    # then
    with pytest.raises(MaximumValidationError):
        instance(11)


def test_fail_validation_with_exclusive_flag() -> None:
    # given
    instance = NumberMaximumValidator(Decimal("10"), exclusive=True)

    # then
    with pytest.raises(MaximumValidationError):
        instance(10)
