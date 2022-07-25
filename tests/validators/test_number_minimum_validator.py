from decimal import Decimal

from pytest import mark

from jsoned.validators import Context, validate_number


@mark.parametrize("value,expected_minimum", [
    [11, Decimal("10")],
    [10.3, Decimal("10.2")],
    [10.2, Decimal("10.2")],
    [0, Decimal("0")],
])
def test_pass_validation(value, expected_minimum: Decimal) -> None:
    context = Context()
    assert validate_number(value, context, expected_minimum=expected_minimum)
    assert not context.errors


@mark.parametrize("value,expected_minimum", [
    [9, Decimal("10")],
    [10.1, Decimal("10.2")],
    [-1, Decimal("0")],
])
def test_fail_validation(value, expected_minimum: Decimal) -> None:
    context = Context()

    assert not validate_number(value, context, expected_minimum=expected_minimum)
    assert context.errors


@mark.parametrize("value,expected_minimum", [
    [10.1, Decimal("10")],
    [9.2, Decimal("9.1")],
    [0, Decimal("-1")],
])
def test_pass_exclusive_validation(value, expected_minimum: Decimal) -> None:
    context = Context()
    assert validate_number(value, context, expected_minimum=expected_minimum, exclusive_comparison=True)
    assert not context.errors


@mark.parametrize("value,expected_minimum", [
    [10, Decimal("10")],
    [10.2, Decimal("10.2")],
    [-1, Decimal("-1")],
])
def test_fail_exclusive_validation(value, expected_minimum: Decimal) -> None:
    context = Context()

    assert not validate_number(value, context, expected_minimum=expected_minimum, exclusive_comparison=True)
    assert context.errors
