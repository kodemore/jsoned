from decimal import Decimal
from typing import List

from pytest import mark

from jsoned.validators import validate_type, Context
from jsoned.validators.core_validators import AssertType


@mark.parametrize("value,expected_types", [
    ["1", [AssertType.STRING]],
    [1, [AssertType.NUMBER]],
    [2, [AssertType.INTEGER]],
    [True, [AssertType.BOOLEAN]],
    [[1, 2, 5], [AssertType.ARRAY]],
    [{"a": 1, "c": 2}, [AssertType.OBJECT]],
    [Decimal("1.2"), [AssertType.NUMBER]],
    [None, [AssertType.NULL]],
    [None, [AssertType.NULL, AssertType.NUMBER]],
    [1, [AssertType.NULL, AssertType.NUMBER]]
])
def test_pass_validation(value, expected_types: List[AssertType]) -> None:
    context = Context()
    assert validate_type(value=value, expected_types=expected_types, context=context)
    assert not context.errors


@mark.parametrize("value,expected_types", [
    ["1", [AssertType.NUMBER]],
    [1, [AssertType.BOOLEAN]],
    [False, [AssertType.NULL]],
])
def test_fail_validation(value, expected_types) -> None:
    context = Context()
    assert not validate_type(value=value, expected_types=expected_types, context=context)
    assert context.errors
