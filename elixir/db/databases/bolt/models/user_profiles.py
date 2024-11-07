# app/plugins/auth/models.py
from . import (
    BaseModel, TABLE_PREFIX,
    User
)

from peewee import CharField, ForeignKeyField


class UserProfiles(BaseModel):
    class Meta:
        table_name = f"{TABLE_PREFIX}_users"

    user = ForeignKeyField(User, unique=True, lazy_load=False)
    color = CharField(
        default="turquoise",
        choices=[
            "blue",
            "red",
            "pink",
            "purple",
            "green",
            "yellow",
            "orange",
            "indigo",
            "turquoise",
        ],
    )
    avatar = CharField(default="incognito")

    def serialize(self):
        return {
            "color": self.color,
            "avatar": self.avatar,
        }

    @classmethod
    def deserialize(cls, data):
        profile = cls()
        profile.color = data.get("color")
        profile.avatar = data.get("avatar")

        return profile
