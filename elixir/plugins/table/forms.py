from flask_wtf import FlaskForm

# from plugins.raven.models import Label
from wtforms import SelectMultipleField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired


class ColumnOrderForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(ColumnOrderForm, self).__init__(*args, **kwargs)

    column_state = StringField(
        label="column_state",
        validators=[InputRequired()],
    )

    submit = SubmitField("Save")
