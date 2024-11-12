from flask_wtf import FlaskForm

# from elixir.plugins.raven.models import Label
from wtforms import SelectMultipleField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired


class PlaceholderForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(PlaceholderForm, self).__init__(*args, **kwargs)
