from .base_pools import main_db, wilo_db
from peewee import Model


# ======================================================================
# Core Models
# DON'T TOUCH! TOUCH THESE INSTEAD (. )( .)
# Tony: I touched both....
# ======================================================================
class BaseModel(Model):
    class Meta:
        database = main_db


class WiLoModel(Model):
    class Meta:
        database = wilo_db
