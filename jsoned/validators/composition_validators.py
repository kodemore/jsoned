from jsoned.errors import ValidationError
from jsoned.validators import Validator
from jsoned.validators.core_validators import Context, CompoundValidator


class AllOfValidator(Validator):
    def __init__(self):
        self.validators = []

    def validate(self, value, context: Context = Context()) -> None:
        for validator in self.validators:
            validator.validate(value, context)


class AnyOfValidator(Validator):
    def __init__(self):
        self.validators = []

    def validate(self, value, context: Context = Context()) -> None:
        last_error = None
        for validator in self.validators:
            try:
                validator.validate(value, context)
                return
            except ValidationError as error:
                last_error = error

        raise last_error


class OneOfValidator(Validator):
    def __init__(self):
        self.validators = []

    def validate(self, value, context: Context = Context()) -> None:
        valid = 0
        last_error = None
        for validator in self.validators:
            try:
                validator.validate(value, context)
                valid += 1
            except ValidationError as error:
                last_error = error

        if valid < 1:
            raise last_error

        if valid > 1:
            raise ValidationError(
                message="Passed value matches more than one expression, exactly one expected.",
                path=context.path
            )


class NotValidator(Validator):
    def __init__(self, validator: Validator):
        self.validator = validator

    def validate(self, value, context: Context = Context()) -> None:
        try:
            self.validator.validate(value, context)
        except ValidationError:
            return
        raise ValidationError("Failed to validate the value.", path=context.path)


class ConditionalValidator(CompoundValidator):
    def validate(self, value, context: Context = Context()) -> None:
        if "if" not in self:
            return

        try:
            self["if"].validate(value, context)
        except ValidationError:
            if "else":
                self["else"].validate(value, context)
                return

        if "then" in self:
            self["then"].validate(value, context)
