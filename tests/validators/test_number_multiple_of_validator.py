from decimal import Decimal

from pytest import mark

from jsoned.validators import Context, validate_number


@mark.parametrize("value,multiple_of", [
    [10, Decimal("10")],
    [10.1, Decimal("0.1")],
    [2.4, Decimal("1.2")],
    [4, Decimal("1")],
    [0, Decimal("1")],
])
def test_pass_validation(value, multiple_of: Decimal) -> None:
    context = Context()
    assert validate_number(value, context, multiple_of=multiple_of)
    assert not context.errors


@mark.parametrize("value,multiple_of", [
    [9, Decimal("10")],
    [10.1, Decimal("10.2")],
    [1.2, Decimal("1.1")],
    [0.35, Decimal("0.1")],
])
def test_fail_validation(value, multiple_of: Decimal) -> None:
    context = Context()
    assert not validate_number(value, context, multiple_of=multiple_of)
    assert context.errors
