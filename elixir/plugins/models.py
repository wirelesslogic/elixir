# Models should be in db.
from elixir.plugins.raven.models import Customers
from elixir.plugins.auth.models import User

def get_model(name: str):
    return globals().get(name)
