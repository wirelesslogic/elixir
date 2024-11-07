Module plugins.auth.fields
==========================

Classes
-------

`AuthenticationCodeField(label='', validators=None, recovery_code_length=12, only_six_digit=False, **kwargs)`
:   Custom WTForms StringField that can validate either a 6-digit code or a recovery code.
    The type of code accepted can be specified upon instantiation.
    
    Construct a new field.
    
    :param label:
        The label of the field.
    :param validators:
        A sequence of validators to call when `validate` is called.
    :param filters:
        A sequence of callable which are run by :meth:`~Field.process`
        to filter or transform the input data. For example
        ``StringForm(filters=[str.strip, str.upper])``.
        Note that filters are applied after processing the default and
        incoming data, but before validation.
    :param description:
        A description for the field, typically used for help text.
    :param id:
        An id to use for the field. A reasonable default is set by the form,
        and you shouldn't need to set this manually.
    :param default:
        The default value to assign to the field, if no form or object
        input is provided. May be a callable.
    :param widget:
        If provided, overrides the widget used to render the field.
    :param dict render_kw:
        If provided, a dictionary which provides default keywords that
        will be given to the widget at render time.
    :param name:
        The HTML name of this field. The default value is the Python
        attribute name.
    :param _form:
        The form holding this field. It is passed by the form itself during
        construction. You should never pass this value yourself.
    :param _prefix:
        The prefix to prepend to the form name of this field, passed by
        the enclosing form during construction.
    :param _translations:
        A translations object providing message translations. Usually
        passed by the enclosing form during construction. See
        :doc:`I18n docs <i18n>` for information on message translations.
    :param _meta:
        If provided, this is the 'meta' instance from the form. You usually
        don't pass this yourself.
    
    If `_form` isn't provided, an :class:`UnboundField` will be
    returned instead. Call its :func:`bind` method with a form instance and
    a name to construct the field.

    ### Ancestors (in MRO)

    * wtforms.fields.simple.StringField
    * wtforms.fields.core.Field

    ### Methods

    `is_valid_recovery_code(self)`
    :   Check if the data is a valid recovery code.

    `is_valid_six_digit_code(self)`
    :   Check if the data is a valid 6-digit code.

    `pre_validate(self, form)`
    :   Pre-validation method to check if the field contains valid data based on the specified mode.