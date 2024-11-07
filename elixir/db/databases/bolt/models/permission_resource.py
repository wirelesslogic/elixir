from . import BaseModel, TABLE_PREFIX

from peewee import CharField, ForeignKeyField


class PermissionResource(BaseModel):
    class Meta:
        table_name = f"{TABLE_PREFIX}_permission_resources"

    name = CharField(max_length=100)
    description = CharField(null=True)
