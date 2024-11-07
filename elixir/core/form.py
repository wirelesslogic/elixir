from flask_wtf import FlaskForm


class BaseForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)

    def set_validation_error(self, field_name, error_message):
        if field_name in self._fields:
            field = self._fields[field_name]
            field.errors.append(error_message)
            return True
        return False
