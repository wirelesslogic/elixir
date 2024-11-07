from redis.commands.search.field import TextField, NumericField

from core.redis_imp import JsonIndexList


seconds_in_day = 86400
default_expiration = seconds_in_day * 2

default_insert_delay_seconds = 2
default_insert_retry = 5

default_reserve_timeout_seconds = 60 * 10

redis_job_key_name: str = "maestro_job"
job_redis_schema: JsonIndexList = {
    "maestro_job": (
        TextField("$.message", as_name="message"),
        TextField("$.job_name", as_name="job_name"),
        TextField("$.tube", as_name="tube"),
        TextField("$.status", as_name="status"),
        NumericField("$.kick_amount", as_name="kick_amount"),
        NumericField("$.bury_amount", as_name="bury_amount"),
        NumericField("$.release_amount", as_name="release_amount"),
        TextField("$.last_error", as_name="last_error"),
    )
}
