from decimal import Decimal

from pytest import mark

from jsoned.validators import validate_const, Context


@mark.parametrize("value,expected_value", [
    ["1", "1"],
    [1, 1],
    [True, True],
    [[1, 2, 5], [1, 2, 5]],
    [{"a": 1, "c": 2}, {"c": 2, "a": 1}],
    [Decimal("1.2"), Decimal("1.2")],
    [None, None]
])
def test_pass_validation(value, expected_value) -> None:
    context = Context()
    assert validate_const(value, context, expected_value=expected_value)
    assert not context.errors


@mark.parametrize("value,expected_value", [
    ["1", ""],
    [1, True],
    [False, 0],
    [[1, 2, 5], [1, 2, 4]],
    [{"a": 2, "c": 2}, {"c": 2, "a": 1}],
    [Decimal("1.3"), Decimal("1.2")]
])
def test_fail_validation(value, expected_value) -> None:
    context = Context()
    assert not validate_const(value, context, expected_value=expected_value)
    assert context.errors
