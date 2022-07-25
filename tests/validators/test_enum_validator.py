from decimal import Decimal

from pytest import mark

from jsoned.validators import validate_enum, Context


@mark.parametrize("value,expected_values", [
    ["1", ["2", "1", "3"]],
    [1, [3, 2, 1]],
    [True, [1, False, True]],
    [False, [True, 0, False]],

    [Decimal("1.2"), [1.2, 1, 2, Decimal("1.2")]],
    [None, [False, 0, None]]
])
def test_pass_validation(value, expected_values) -> None:
    context = Context()
    assert validate_enum(value=value, expected_values=expected_values, context=context)
    assert not context.errors


@mark.parametrize("value,expected_values", [
    ["1", ["2", "3"]],
    [1, [3, 2]],
    [True, [1, False]],
    [False, [True, 0]],

    [Decimal("1.2"), [1.2, 1, 2]],
    [None, [False, 0]]
])
def test_fail_validation(value, expected_values) -> None:
    context = Context()
    assert not validate_enum(value=value, expected_values=expected_values, context=context)
    assert context.errors
