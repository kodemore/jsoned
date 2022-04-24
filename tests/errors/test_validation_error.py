from jsoned.errors import ValidationError


def test_can_instantiate() -> None:
    # given
    instance = ValidationError("Test message")

    # then
    assert isinstance(instance, ValidationError)


def test_can_subclass_with_parameters() -> None:
    # given
    class CustomValidationError(ValidationError):
        message = "Some problem: {custom_field}"
        custom_field: str

    # when
    instance = CustomValidationError(custom_field="A")

    # then
    assert instance.custom_field == "A"
    assert str(instance) == "Failed validation at ``. Some problem: A"
