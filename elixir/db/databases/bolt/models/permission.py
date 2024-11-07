from . import (
    BaseModel, TABLE_PREFIX,
    PermissionResource,
    PermissionAction
)

from peewee import CharField, ForeignKeyField


class Permission(BaseModel):
    class Meta:
        table_name = f"{TABLE_PREFIX}_permission_actions"

    name = CharField(max_length=100)
    description = CharField(null=True)
    resource = ForeignKeyField(PermissionResource)
    action = ForeignKeyField(PermissionAction)
