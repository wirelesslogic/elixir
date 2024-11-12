from playhouse.pool import (
    PooledDatabase
)
from elixir.core.logger import log
from .base_pools import (
    wilo_db,
    main_db
)

def connect_to_db(db: PooledDatabase) -> bool:
    try:
        db.connect()

        return True
    except Exception as e:
        log.error(e)

    finally:
        return False
