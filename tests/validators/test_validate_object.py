from jsoned.errors.validation_error import ValidationError
from jsoned.validators import ValidatorsMap, create_string_validator, validate_object, Context


def test_validate_object_properties() -> None:
    properties = ValidatorsMap[str]()
    properties["name"] = create_string_validator(expected_minimum_length=1, expected_maximum_length=10)

    context = Context()
    assert not validate_object({"name": ""}, context, expected_properties=properties)
    assert context.errors[0].path == "name"
    assert context.errors[0].code == ValidationError.ErrorCodes.STRING_MINIMUM_LENGTH_ERROR

    assert validate_object({"name": "Bob"}, expected_properties=properties)


def test_validate_additional_properties() -> None:
    properties = ValidatorsMap[str]()
    properties["name"] = create_string_validator(expected_minimum_length=1, expected_maximum_length=10)
