from decimal import Decimal

import pytest

from jsoned.errors import MultipleOfValidationError
from jsoned.validators.number_validators import NumberMultipleOfValidator


def test_can_instantiate() -> None:
    # given
    instance = NumberMultipleOfValidator(Decimal("10"))

    # then
    assert isinstance(instance, NumberMultipleOfValidator)


def test_pass_validation() -> None:
    # given
    instance = NumberMultipleOfValidator(Decimal("10"))

    # then
    instance(10)
    instance(20)


def test_fail_validation() -> None:
    # given
    instance = NumberMultipleOfValidator(Decimal("10"))

    # then
    with pytest.raises(MultipleOfValidationError):
        instance("11")
