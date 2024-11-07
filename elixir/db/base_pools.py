from playhouse.pool import (
    PooledPostgresqlExtDatabase,
    PooledMySQLDatabase
)

# Create a database instance, but don't bind
# to any specific database yet. This way we can
# change the database for unit tests.
main_db = PooledPostgresqlExtDatabase(None)
wilo_db = PooledMySQLDatabase(None)
