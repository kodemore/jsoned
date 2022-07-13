import re
from functools import partial

from jsoned.validators import Context
from jsoned.validators.string_validators import validate_string


def test_pass_validation() -> None:
    # given
    context = Context()
    validate = partial(validate_string, context=context, expected_pattern=re.compile("[a-z]+"))

    # then
    assert validate("abcd")
    assert validate("bcd")
    assert not context.errors


def test_fail_validation() -> None:
    # given
    context = Context()
    validate = partial(validate_string, context=context, expected_pattern=re.compile("[a-z]+"))

    # then
    assert not validate("123")
    assert context.errors
