from . import (
    BaseModel, TABLE_PREFIX,
    Role,
    Permission
)

from peewee import ForeignKeyField


class RolePermission(BaseModel):
    class Meta:
        table_name = f"{TABLE_PREFIX}_map_roles_permissions"
        indexes = (
            # Specify a unique multi-column index
            (("role", "permission"), True),
        )

    role = ForeignKeyField(Role)
    permission = ForeignKeyField(Permission)


