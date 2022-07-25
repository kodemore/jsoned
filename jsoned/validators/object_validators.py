from typing import List, Pattern, Dict, Mapping

from jsoned.errors import ValidationError
from jsoned.validators.composition_validators import validate_all
from jsoned.validators.core_validators import Validator, Context, AssertType, ValidatorsMap, ValidatorsCollection


def validate_object_properties(
    value: Mapping,
    context: Context,
    properties: ValidatorsMap[str] = None,
    property_names: Validator = None,
    additional_properties: Validator = None,
    pattern_properties: ValidatorsMap[Pattern] = None,
    unevaluated_properties: bool = True,
) -> bool:
    # ignore non-object values
    if not isinstance(value, dict):
        return True

    for name, item in value.items():
        found = False
        if properties and name in properties:
            if not properties[name](item, context + name):
                return False
            found = True

        # pattern properties can invalidate properties
        if pattern_properties:
            for pattern, validator in pattern_properties.items():
                if pattern.search(name):
                    if not validator(item, context + name):
                        return False
                    else:
                        found = True

        # if property already validated by property or pattern property we should
        # move to next property
        if found:
            continue

        property_name_context = context.with_path()
        if property_names and not property_names(name, property_name_context + name):
            context.errors.append(
                ValidationError.for_property_name(
                    path=context.path,
                    property_name=name,
                    reason=property_name_context.errors[0]
                )
            )
            return False

        if additional_properties:
            if not additional_properties(item, Context()):
                context.errors.append(ValidationError.for_additional_property(path=(context + name).path, property_name=name))
                return False
            continue

        if not unevaluated_properties:
            context.errors.append(ValidationError.for_unevaluated_property(path=context.path, property_name=name))
            return False

    return True


def validate_required_properties(value: Mapping, context: Context, expected_properties: List[str]) -> bool:
    if not isinstance(value, dict):  # ignore non-objects
        return True

    for name in expected_properties:
        if name in value:
            continue

        context.errors.append(ValidationError.for_missing_property(context.path, property_name=name))
        return False

    return True


def validate_dependent_required_properties(value, context: Context, dependency_map: Dict[str, List[str]]) -> bool:
    if not isinstance(value, dict):  # ignore non-objects
        return True

    for name, dependants in dependency_map.items():
        if name not in value:
            continue

        for dependent_property in dependants:
            if dependent_property not in value:
                context.errors.append(
                    ValidationError.for_missing_property(context.path, property_name=dependent_property)
                )
                return False

    return True


def validate_dependent_schemas(value, context: Context, dependent_schemas: ValidatorsMap[str]) -> bool:
    if not isinstance(value, dict):  # ignore non-objects
        return True

    for schema_property, validator in dependent_schemas.items():
        if schema_property not in value:
            continue

        if not validator(value, context + schema_property):
            return False

    return True


def validate_minimum_properties(value, context, expected_minimum: int) -> bool:
    if not isinstance(value, dict):  # ignore non-objects
        return True

    if len(value) < expected_minimum:
        context.errors.append(ValidationError.for_property_minimum_length(context, expected_minimum=expected_minimum))
        return False

    return True


def validate_maximum_properties(value, context, expected_maximum: int) -> bool:
    if not isinstance(value, dict):  # ignore non-objects
        return True

    if len(value) > expected_maximum:
        context.errors.append(ValidationError.for_property_maximum_length(context, expected_maximum=expected_maximum))
        return False

    return True


def validate_object(
    value,
    context: Context = None,
    expected_properties: ValidatorsMap[str] = None,
    additional_properties: Validator = None,
    pattern_properties: ValidatorsMap[Pattern] = None,
    unevaluated_properties: bool = True,
    required_properties: List[str] = None,
    expected_property_names: Validator = None,
    dependent_required_properties: Dict[str, List[str]] = None,
    dependent_schemas: ValidatorsMap[str] = None,
    expected_minimum_properties: int = 0,
    expected_maximum_properties: int = 0,
) -> bool:
    context = context or Context()
    return create_object_validator(
        expected_properties,
        additional_properties,
        pattern_properties,
        unevaluated_properties,
        required_properties,
        expected_property_names,
        dependent_required_properties,
        dependent_schemas,
        expected_minimum_properties,
        expected_maximum_properties
    )(value, context)


def create_object_validator(
    expected_properties: ValidatorsMap[str] = None,
    additional_properties: Validator = None,
    pattern_properties: ValidatorsMap[Pattern] = None,
    unevaluated_properties: bool = True,
    required_properties: List[str] = None,
    expected_property_names: Validator = None,
    dependent_required_properties: Dict[str, List[str]] = None,
    dependent_schemas: ValidatorsMap[str] = None,
    expected_minimum_properties: int = 0,
    expected_maximum_properties: int = 0,
) -> Validator:

    validators = ValidatorsCollection()

    if expected_properties or additional_properties or pattern_properties or expected_property_names:
        validators.append(
            validate_object_properties,
            properties=expected_properties,
            pattern_properties=pattern_properties,
            unevaluated_properties=unevaluated_properties,
            property_names=expected_property_names,
            additional_properties=additional_properties,
        )

    if required_properties:
        validators.append(
            validate_required_properties,
            expected_properties=required_properties
        )

    if dependent_required_properties:
        validators.append(
            validate_dependent_required_properties,
            dependency_map=dependent_required_properties
        )

    if dependent_schemas:
        validators.append(
            validate_dependent_schemas,
            dependent_schemas=dependent_schemas
        )

    if expected_minimum_properties > 0:
        validators.append(
            validate_minimum_properties,
            expected_minimum=expected_minimum_properties
        )

    if expected_maximum_properties > 0:
        validators.append(
            validate_maximum_properties,
            expected_maximum=expected_maximum_properties
        )

    def _validate_object(value, context: Context) -> bool:
        if not isinstance(value, Mapping):
            context.errors.append(ValidationError.for_type(context.path, expected_types=[str(AssertType.OBJECT)]))
            return False

        return validate_all(value, context, validators)

    return _validate_object
