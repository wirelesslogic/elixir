from apispec import APISpec
from apispec_webframeworks.flask import FlaskPlugin


def create_api_spec_obj(title: str, info: dict | None = None, version: str = "0.1") -> APISpec:
    info_dict = info if info is not None else {}

    return APISpec(
        title=title,
        info=info_dict,
        version=version,
        openapi_version="3.1.0",
    )
