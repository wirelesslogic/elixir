from redis import Redis, ConnectionPool
from redis.client import Pipeline
from redis.commands.json.path import Path
from redis.commands.search.field import Field
from redis.commands.search.query import Query
from redis.commands.search.indexDefinition import IndexType, IndexDefinition
from redis.commands.search.result import Result


JsonIndexSchema = tuple[Field, ...]
JsonIndexList = dict[str, JsonIndexSchema]


# Might want to make better use of the connection pool by implementing a get_connection
# and saving the connection pool instead of a single redisConnection.
class RedisImp:
    redisConnection: Redis
    indexes: list[str]

    def __init__(self, pool):
        self.redisConnection = Redis.from_pool(connection_pool=pool)
        self.redisConnection.ping()

        self.get_indexes()

    def get_execution_target(self, pipeline: Pipeline | None = None):
        return self.redisConnection.pipeline() if pipeline is None else pipeline

    @staticmethod
    def make_index_key(input_str: str) -> str:
        return f'idx:{input_str}'

    @staticmethod
    def make_prefix(input_str: str) -> str:
        return f"{input_str}:"

    @staticmethod
    def create_connection_pool(host: str, port: int) -> ConnectionPool:
        return ConnectionPool(host=host, port=port, decode_responses=True)

    def prepare_json_indexes(self, index_schemas: JsonIndexList, hard_reset: bool = False):
        pipeline = self.redisConnection.pipeline()

        for key, index_schema in index_schemas.items():
            index_key = self.make_index_key(key)
            index_prefix = self.make_prefix(key)

            if index_key in self.indexes:
                if not hard_reset:
                    continue

                self.remove_json_index(index_key)

            self.create_json_index(index_key, index_prefix, index_schema)

        pipeline.execute()

    def create_json_index(
            self,
            index_key: str,
            index_prefix: str,
            schema: JsonIndexSchema,
            pipeline: Pipeline | None = None
    ):
        exec_target = self.get_execution_target(pipeline)

        exec_target.ft(index_key).create_index(
            schema,
            definition=IndexDefinition(
                prefix=[index_prefix], index_type=IndexType.JSON
            )
        )

    def remove_json_index(self, index_name: str, pipeline: Pipeline | None = None):
        exec_target = self.get_execution_target(pipeline)

        exec_target.ft(index_name).dropindex(True)

    def set_json_value(self, key: str, value: dict, expiration_seconds: int | None = None, pipeline: Pipeline | None = None) -> None:
        exec_target = self.get_execution_target(pipeline)

        exec_target.json().set(
            key,
            Path.root_path(),
            value
        )

        if expiration_seconds is not None:
            exec_target.expire(name=key, time=expiration_seconds)

        exec_target.execute()

    def search_index(
            self,
            index_name: str,
            query: Query,
            query_params: dict[str, str | int | float | bytes] | None = None,
    ) -> Result:
        return self.redisConnection.ft(index_name).search(
            query,
            query_params
        )

    def get_json_value(self, key: str):
        return self.redisConnection.get(key)

    def get_indexes(self):
        self.indexes = self.redisConnection.execute_command("FT._LIST")
