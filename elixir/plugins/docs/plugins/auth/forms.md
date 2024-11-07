Module plugins.auth.forms
=========================

Classes
-------

`LoginForm(*args, **kwargs)`
:   Flask-specific subclass of WTForms :class:`~wtforms.form.Form`.
    
    If ``formdata`` is not specified, this will use :attr:`flask.request.form`
    and :attr:`flask.request.files`.  Explicitly pass ``formdata=None`` to
    prevent this.
    
    :param formdata: Input data coming from the client, usually
        ``request.form`` or equivalent. Should provide a "multi
        dict" interface to get a list of values for a given key,
        such as what Werkzeug, Django, and WebOb provide.
    :param obj: Take existing data from attributes on this object
        matching form field attributes. Only used if ``formdata`` is
        not passed.
    :param prefix: If provided, all fields will have their name
        prefixed with the value. This is for distinguishing multiple
        forms on a single page. This only affects the HTML name for
        matching input data, not the Python name for matching
        existing data.
    :param data: Take existing data from keys in this dict matching
        form field attributes. ``obj`` takes precedence if it also
        has a matching attribute. Only used if ``formdata`` is not
        passed.
    :param meta: A dict of attributes to override on this form's
        :attr:`meta` instance.
    :param extra_filters: A dict mapping field attribute names to
        lists of extra filter functions to run. Extra filters run
        after filters passed when creating the field. If the form
        has ``filter_<fieldname>``, it is the last extra filter.
    :param kwargs: Merged with ``data`` to allow passing existing
        data as parameters. Overwrites any duplicate keys in
        ``data``. Only used if ``formdata`` is not passed.

    ### Ancestors (in MRO)

    * core.form.BaseForm
    * flask_wtf.form.FlaskForm
    * wtforms.form.Form
    * wtforms.form.BaseForm

    ### Class variables

    `email`
    :

    `password`
    :

    `remember_me`
    :

    `submit`
    :

`OTPForm(*args, **kwargs)`
:   Flask-specific subclass of WTForms :class:`~wtforms.form.Form`.
    
    If ``formdata`` is not specified, this will use :attr:`flask.request.form`
    and :attr:`flask.request.files`.  Explicitly pass ``formdata=None`` to
    prevent this.
    
    :param formdata: Input data coming from the client, usually
        ``request.form`` or equivalent. Should provide a "multi
        dict" interface to get a list of values for a given key,
        such as what Werkzeug, Django, and WebOb provide.
    :param obj: Take existing data from attributes on this object
        matching form field attributes. Only used if ``formdata`` is
        not passed.
    :param prefix: If provided, all fields will have their name
        prefixed with the value. This is for distinguishing multiple
        forms on a single page. This only affects the HTML name for
        matching input data, not the Python name for matching
        existing data.
    :param data: Take existing data from keys in this dict matching
        form field attributes. ``obj`` takes precedence if it also
        has a matching attribute. Only used if ``formdata`` is not
        passed.
    :param meta: A dict of attributes to override on this form's
        :attr:`meta` instance.
    :param extra_filters: A dict mapping field attribute names to
        lists of extra filter functions to run. Extra filters run
        after filters passed when creating the field. If the form
        has ``filter_<fieldname>``, it is the last extra filter.
    :param kwargs: Merged with ``data`` to allow passing existing
        data as parameters. Overwrites any duplicate keys in
        ``data``. Only used if ``formdata`` is not passed.

    ### Ancestors (in MRO)

    * core.form.BaseForm
    * flask_wtf.form.FlaskForm
    * wtforms.form.Form
    * wtforms.form.BaseForm

    ### Class variables

    `auth_code`
    :

    `submit`
    :

`SignupForm(*args, **kwargs)`
:   Flask-specific subclass of WTForms :class:`~wtforms.form.Form`.
    
    If ``formdata`` is not specified, this will use :attr:`flask.request.form`
    and :attr:`flask.request.files`.  Explicitly pass ``formdata=None`` to
    prevent this.
    
    :param formdata: Input data coming from the client, usually
        ``request.form`` or equivalent. Should provide a "multi
        dict" interface to get a list of values for a given key,
        such as what Werkzeug, Django, and WebOb provide.
    :param obj: Take existing data from attributes on this object
        matching form field attributes. Only used if ``formdata`` is
        not passed.
    :param prefix: If provided, all fields will have their name
        prefixed with the value. This is for distinguishing multiple
        forms on a single page. This only affects the HTML name for
        matching input data, not the Python name for matching
        existing data.
    :param data: Take existing data from keys in this dict matching
        form field attributes. ``obj`` takes precedence if it also
        has a matching attribute. Only used if ``formdata`` is not
        passed.
    :param meta: A dict of attributes to override on this form's
        :attr:`meta` instance.
    :param extra_filters: A dict mapping field attribute names to
        lists of extra filter functions to run. Extra filters run
        after filters passed when creating the field. If the form
        has ``filter_<fieldname>``, it is the last extra filter.
    :param kwargs: Merged with ``data`` to allow passing existing
        data as parameters. Overwrites any duplicate keys in
        ``data``. Only used if ``formdata`` is not passed.

    ### Ancestors (in MRO)

    * core.form.BaseForm
    * flask_wtf.form.FlaskForm
    * wtforms.form.Form
    * wtforms.form.BaseForm

    ### Class variables

    `confirm`
    :

    `email`
    :

    `name`
    :

    `password`
    :

    `submit`
    :