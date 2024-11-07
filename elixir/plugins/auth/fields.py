from wtforms import StringField
from wtforms.validators import ValidationError


class AuthenticationCodeField(StringField):
    """
    Custom WTForms StringField that can validate either a 6-digit code or a recovery code.
    The type of code accepted can be specified upon instantiation.
    """

    def __init__(
        self,
        label="",
        validators=None,
        recovery_code_length=12,
        only_six_digit=False,
        **kwargs
    ):
        super().__init__(label, validators=validators, **kwargs)
        self.recovery_code_length = recovery_code_length
        self.only_six_digit = only_six_digit

    def pre_validate(self, form):
        """
        Pre-validation method to check if the field contains valid data based on the specified mode.
        """
        if self.only_six_digit:
            if not self.is_valid_six_digit_code():
                raise ValidationError("Field must contain exactly 6 digits.")
        else:
            if not (self.is_valid_six_digit_code() or self.is_valid_recovery_code()):
                raise ValidationError(
                    "Field must contain either exactly 6 digits or a valid recovery code."
                )

    def is_valid_six_digit_code(self):
        """
        Check if the data is a valid 6-digit code.
        """
        return self.data.isdigit() and len(self.data) == 6

    def is_valid_recovery_code(self):
        """
        Check if the data is a valid recovery code.
        """
        # Implement recovery code validation logic here.
        return len(self.data) == self.recovery_code_length and all(
            c in "0123456789abcdef" for c in self.data
        )
