from requests import post, Response

from ..config import cfg
from ..auth.hmac_sig import HmacInfo

from . import JobInfo

base_url = f"https://{cfg.maestro.composer.host_name}"


def handle_insert(job_info: JobInfo, hmac_override: HmacInfo = None) -> Response:
    if hmac_override is not None:
        hmac_info = hmac_override
    else:
        hmac_info = HmacInfo(cfg.hmac_secret, cfg.hmac_message)

    url = f"{base_url}/insert/{job_info.name}/{job_info.tube}"
    headers = {"Authorization": hmac_info.make_header()}

    return post(
        url,
        headers=headers,
        json=job_info.data,
    )
