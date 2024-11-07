from . import (
    BaseModel, TABLE_PREFIX,
    User,
    Role
)

from peewee import ForeignKeyField


class UserRole(BaseModel):
    class Meta:
        table_name = f"{TABLE_PREFIX}_permission_actions"
        indexes = (
            # Specify a unique multi-column index
            (("user", "role"), True),
        )
    
    user = ForeignKeyField(User)
    role = ForeignKeyField(Role)
