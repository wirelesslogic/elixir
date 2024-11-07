# app/plugins/auth/models.py
from datetime import datetime

from config import cfg
from . import BaseModel, TABLE_PREFIX, SecureField

from flask_login import UserMixin
from peewee import BooleanField, CharField, DateField
from playhouse.hybrid import hybrid_property
from werkzeug.security import check_password_hash, generate_password_hash


class User(UserMixin, BaseModel):
    class Meta:
        table_name = f"{TABLE_PREFIX}_users"

    uuid = CharField(max_length=12, unique=True)
    name = CharField(max_length=100)
    email = CharField(max_length=128, unique=True)
    password_hash = CharField(max_length=255)
    is_otp_enabled = BooleanField(default=False)
    otp_secret = SecureField(crypto_key=cfg["crypto_key"], null=True)
    otp_recovery_codes = SecureField(crypto_key=cfg["crypto_key"], null=True)
    created_on = DateField(default=datetime.now)
    last_login = DateField(default=datetime.now)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._permissions = None
        self._profile = None

    def get_id(self):
        """Needs to be implemented for flask_login"""
        return str(self.uuid)

    @hybrid_property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def profile(self):
        if not self._profile:
            self._profile = self._fetch_profile()

        return self._profile

    @property
    def permissions(self):
        if not self._permissions:
            self._permissions = self._fetch_permissions()

        return self._permissions

    def _fetch_profile(self):
        return self.userprofiles_set.get_or_none()

    def _fetch_permissions(self):
        permissions_query = (
            Permission.select(
                PermissionResource.name,
                PermissionAction.name,
            )
            .join_from(Permission, PermissionResource)
            .join_from(Permission, PermissionAction)
            .join_from(Permission, RolePermission)
            .join_from(RolePermission, Role)
            .join_from(Role, UserRole)
            .join_from(UserRole, User)
            .where(UserRole.user == self)
        )

        permissions = {}
        for perm in permissions_query:
            resource = perm.permissionresource.name
            action = perm.permissionaction.name
            if resource not in permissions:
                permissions[resource] = set()
            permissions[resource].add(action)

        return permissions

    def serialize(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "email": self.email,
            "is_otp_enabled": self.is_otp_enabled,
            "last_login": self.last_login.isoformat(),
            "profile": self.profile.serialize(),
            "permissions": self.permissions,
        }

    @classmethod
    def deserialize(cls, data):
        user = cls()
        user.uuid = data.get("uuid")
        user.name = data.get("name")
        user.email = data.get("email")
        user.is_otp_enabled = data.get("is_otp_enabled")
        user.last_login = datetime.fromisoformat(data.get("last_login"))

        user._profile = UserProfiles.deserialize(data.get("profile"))
        user._permissions = data.get("permissions", {})

        return user
