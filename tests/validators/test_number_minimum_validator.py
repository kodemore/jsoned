from decimal import Decimal

import pytest

from jsoned.errors import MinimumValidationError
from jsoned.validators.number_validators import NumberMinimumValidator


def test_can_instantiate() -> None:
    # given
    instance = NumberMinimumValidator(Decimal("10"))

    # then
    assert isinstance(instance, NumberMinimumValidator)


def test_pass_validation() -> None:
    # given
    instance = NumberMinimumValidator(Decimal("10"))

    # then
    instance(10)
    instance(20)


def test_pass_validation_with_exclusive_flag() -> None:
    # given
    instance = NumberMinimumValidator(Decimal("10"), exclusive=True)

    # then
    instance(11)
    instance(20)


def test_fail_validation() -> None:
    # given
    instance = NumberMinimumValidator(Decimal("10"))

    # then
    with pytest.raises(MinimumValidationError):
        instance(9)


def test_fail_validation_with_exclusive_flag() -> None:
    # given
    instance = NumberMinimumValidator(Decimal("10"), exclusive=True)

    # then
    with pytest.raises(MinimumValidationError):
        instance(10)
