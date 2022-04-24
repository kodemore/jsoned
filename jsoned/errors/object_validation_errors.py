from jsoned.errors.validation_error import ValidationError


class RequiredPropertyValidationError(ValidationError):
    expected_property: str
    code = "required_property_error"
    message = "Passed value is missing property `{expected_property}`."


class ObjectSizeValidationError(ValidationError):
    pass


class MinimumPropertiesValidationError(ObjectSizeValidationError):
    expected_minimum: int
    code = "minimum_properties_error"
    message = "The number of properties is lower than expected minimum: {expected_minimum}."


class MaximumPropertiesValidationError(ObjectSizeValidationError):
    expected_maximum: int
    code = "maximum_properties_error"
    message = "The number of properties is greater than expected maximum: {expected_maximum}."

