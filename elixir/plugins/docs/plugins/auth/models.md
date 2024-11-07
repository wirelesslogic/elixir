Module plugins.auth.models
==========================

Classes
-------

`Permission(*args, **kwargs)`
:   

    ### Ancestors (in MRO)

    * core.db.models.BaseModel
    * peewee.Model
    * peewee._metaclass_helper_
    * peewee.Node

    ### Class variables

    `DoesNotExist`
    :   Common base class for all non-exit exceptions.

    `action`
    :

    `action_id`
    :

    `description`
    :

    `id`
    :

    `name`
    :

    `resource`
    :

    `resource_id`
    :

    ### Instance variables

    `rolepermission_set`
    :

`PermissionAction(*args, **kwargs)`
:   

    ### Ancestors (in MRO)

    * core.db.models.BaseModel
    * peewee.Model
    * peewee._metaclass_helper_
    * peewee.Node

    ### Class variables

    `DoesNotExist`
    :   Common base class for all non-exit exceptions.

    `description`
    :

    `id`
    :

    `name`
    :

    ### Instance variables

    `permission_set`
    :

`PermissionResource(*args, **kwargs)`
:   

    ### Ancestors (in MRO)

    * core.db.models.BaseModel
    * peewee.Model
    * peewee._metaclass_helper_
    * peewee.Node

    ### Class variables

    `DoesNotExist`
    :   Common base class for all non-exit exceptions.

    `description`
    :

    `id`
    :

    `name`
    :

    ### Instance variables

    `permission_set`
    :

`Role(*args, **kwargs)`
:   

    ### Ancestors (in MRO)

    * core.db.models.BaseModel
    * peewee.Model
    * peewee._metaclass_helper_
    * peewee.Node

    ### Class variables

    `DoesNotExist`
    :   Common base class for all non-exit exceptions.

    `description`
    :

    `id`
    :

    `name`
    :

    ### Instance variables

    `rolepermission_set`
    :

    `userrole_set`
    :

`RolePermission(*args, **kwargs)`
:   

    ### Ancestors (in MRO)

    * core.db.models.BaseModel
    * peewee.Model
    * peewee._metaclass_helper_
    * peewee.Node

    ### Class variables

    `DoesNotExist`
    :   Common base class for all non-exit exceptions.

    `id`
    :

    `permission`
    :

    `permission_id`
    :

    `role`
    :

    `role_id`
    :

`User(*args, **kwargs)`
:   This provides default implementations for the methods that Flask-Login
    expects user objects to have.

    ### Ancestors (in MRO)

    * flask_login.mixins.UserMixin
    * core.db.models.BaseModel
    * peewee.Model
    * peewee._metaclass_helper_
    * peewee.Node

    ### Class variables

    `DoesNotExist`
    :   Common base class for all non-exit exceptions.

    `created_on`
    :

    `email`
    :

    `id`
    :

    `is_otp_enabled`
    :

    `last_login`
    :

    `name`
    :

    `otp_recovery_codes`
    :

    `otp_secret`
    :

    `password_hash`
    :

    `uuid`
    :

    ### Static methods

    `deserialize(data)`
    :

    ### Instance variables

    `password`
    :

    `permissions`
    :

    `profile`
    :

    `userprofiles_set`
    :

    `userrole_set`
    :

    ### Methods

    `get_id(self)`
    :   Needs to be implemented for flask_login

    `serialize(self)`
    :

    `verify_password(self, password)`
    :

`UserProfiles(*args, **kwargs)`
:   

    ### Ancestors (in MRO)

    * core.db.models.BaseModel
    * peewee.Model
    * peewee._metaclass_helper_
    * peewee.Node

    ### Class variables

    `DoesNotExist`
    :   Common base class for all non-exit exceptions.

    `avatar`
    :

    `color`
    :

    `id`
    :

    `user`
    :

    `user_id`
    :

    ### Static methods

    `deserialize(data)`
    :

    ### Methods

    `serialize(self)`
    :

`UserRole(*args, **kwargs)`
:   

    ### Ancestors (in MRO)

    * core.db.models.BaseModel
    * peewee.Model
    * peewee._metaclass_helper_
    * peewee.Node

    ### Class variables

    `DoesNotExist`
    :   Common base class for all non-exit exceptions.

    `id`
    :

    `role`
    :

    `role_id`
    :

    `user`
    :

    `user_id`
    :