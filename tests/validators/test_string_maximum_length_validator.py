from functools import partial

from jsoned.validators import Context
from jsoned.validators.string_validators import validate_string


def test_pass_validation() -> None:
    # given
    context = Context()
    validate = partial(validate_string, context=context, expected_maximum_length=3)

    # then
    assert validate("abc")
    assert validate("bc")
    assert not context.errors


def test_fail_validation() -> None:
    # given
    context = Context()
    validate = partial(validate_string, context=context, expected_maximum_length=2)

    # then
    assert not validate("abc")
    assert context.errors
