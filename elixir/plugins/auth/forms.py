from elixir.core.form import BaseForm
from elixir.plugins.auth.fields import AuthenticationCodeField
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import Email, EqualTo, InputRequired, Length, Optional


class SignupForm(BaseForm):
    name = StringField("Name", validators=[InputRequired()])
    email = StringField(
        "Email",
        validators=[
            Length(min=6),
            Email(message="Enter a valid email."),
            InputRequired(),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
            Length(min=6, message="Select a stronger password."),
        ],
    )
    confirm = PasswordField(
        "Confirm Your Password",
        validators=[
            InputRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )

    submit = SubmitField("Sign Up")


class LoginForm(BaseForm):
    email = StringField(
        "Email", validators=[InputRequired(), Email(message="Enter a valid email.")]
    )
    password = PasswordField("Password", validators=[InputRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Log In")


class OTPForm(BaseForm):
    auth_code = AuthenticationCodeField("Enter code")
    submit = SubmitField("Verify")
