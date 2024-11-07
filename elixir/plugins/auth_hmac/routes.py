from core import log
from core.auth import AuthenticationMethodHmac
from config import cfg

from flask import (
    Blueprint,
    current_app,
    request,
    jsonify,
)

plugin = Blueprint("auth_hmac", __name__, template_folder="templates")


# Endpoints added to this set ARE checked
hmac_endpoints = set()


def use_hmac(namespace):
    def wrapper(func):
        hmac_endpoints.add(f"{namespace}.{func.__name__}")
        log.info(f"Endpoint HMAC requirement registered: {namespace}.{func.__name__}")

        return func

    return wrapper


@plugin.before_app_request
def hmac_required():
    # log.info(f"HMAC check for: {request.endpoint}")
    if request.endpoint in hmac_endpoints:
        incoming_signature = AuthenticationMethodHmac.split_hmac_header(
            request.headers.get("Authorization", "")
        )

        secret = bytearray()
        # Should be secret
        secret.extend(map(ord, cfg.hmac_secret))

        message = cfg.hmac_message.encode("ascii")

        passing = AuthenticationMethodHmac.validate_incoming_signature(
            incoming_signature, secret, message
        )

        if passing:
            return

        return jsonify({"message": "You shall not pass."}), 401

    return
