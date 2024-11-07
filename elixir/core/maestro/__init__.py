from typing import Any
from pydantic import ValidationError
import greenstalk
import json

from ..redis_imp import RedisImp

from .. import log

from .types import JobList


class JobInfo:
    def __init__(self, tube: str, name: str, data: dict):
        self.tube = tube
        self.name = name
        self.data = data

    def prepare(self):
        return {
            "tube": self.tube,
            "name": self.name,
            "data": self.data,
        }


class JobUtils:
    @staticmethod
    def decode_body(job: greenstalk.Job) -> Any:
        return json.loads(job.body)

    @staticmethod
    def encode_body(job: JobInfo) -> str:
        return json.dumps(job.prepare())

    @staticmethod
    def validate_data(job: JobInfo, job_list: JobList) -> tuple[bool, str]:
        validator = job_list.get(job.name, None)

        if validator is None:
            msg = "Validator not found"
            log.error(f"{job.name} | {msg}")
            return False, msg

        try:
            validator.model_validate(job.data)
        except ValidationError as e:
            log.error(e)
            return False, e

        return True, ""


class Reporter:
    @staticmethod
    def report_status(
        stalk_client: greenstalk.Client,
        redis_instance: RedisImp,
        redis_key_prefix: str,
        job: greenstalk.Job,
        message: str,
        status: str,
        last_error: str | None = None,
        expiration_seconds: int | None = None,
    ) -> None:
        data = JobUtils.decode_body(job)
        job_info = stalk_client.stats_job(job)

        input_value = Reporter.prepare_data(data, job_info, message, status, last_error)

        redis_instance.set_json_value(
            key=f"{redis_key_prefix}{job.id}",
            value=input_value,
            expiration_seconds=expiration_seconds,
        )

    @staticmethod
    def prepare_data(
        data: dict | None,
        job_info: dict[str, str | int],
        message: str,
        status: str,
        last_error: str | None = None,
    ):
        return {
            "message": message,
            "job_name": data.get("name", None),
            "tube": data.get("tube", None),
            "data": data,
            "status": status,
            "kick_amount": job_info.get("kicks", -1),
            "bury_amount": job_info.get("buries", -1),
            "release_amount": job_info.get("releases", -1),
            "last_error": last_error,
        }
