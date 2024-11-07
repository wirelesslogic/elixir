from . import (
    BaseModel, TABLE_PREFIX
)

from peewee import CharField, ForeignKeyField


class PermissionAction(BaseModel):
    class Meta:
        table_name = f"{TABLE_PREFIX}_permission_actions"

    name = CharField(max_length=100)
    description = CharField(null=True)
