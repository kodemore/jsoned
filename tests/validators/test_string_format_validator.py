from jsoned.string_format import StringFormat
from jsoned.validators import Context
from jsoned.validators.string_validators import validate_string


def test_pass_validation() -> None:
    # given
    context = Context()

    # when
    assert validate_string("test@test.com", context=context, expected_format=StringFormat.EMAIL)
    assert validate_string("true", context=context, expected_format=StringFormat.BOOLEAN)
    assert validate_string("2020-10-19", context=context, expected_format=StringFormat.DATE)
    assert validate_string("2020-10-19T15:12:10", context=context, expected_format=StringFormat.DATE_TIME)
    assert validate_string("http://test.com", context=context, expected_format=StringFormat.URL)

    # then
    assert not context.errors


def test_fail_validation() -> None:
    assert validate_string("test@test.com", expected_format=StringFormat.EMAIL)
