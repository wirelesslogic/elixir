from . import BaseModel, TABLE_PREFIX

from peewee import CharField


class Role(BaseModel):
    class Meta:
        table_name = f"{TABLE_PREFIX}_roles"

    name = CharField(max_length=100)
    description = CharField(null=True)
