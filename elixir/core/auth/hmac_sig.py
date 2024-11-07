import base64
import hashlib
import hmac

from typing_extensions import Buffer

from .authentication_method import AuthenticationMethod


class AuthenticationMethodHmac(AuthenticationMethod):
    @staticmethod
    def handle_key(received_key) -> tuple[bool, str]:
        return (
            False,
            "Not implemented",
        )

    @staticmethod
    def prepare_secret(secret: str) -> bytearray:
        secret_array = bytearray()
        secret_array.extend(map(ord, secret))

        return secret_array

    @staticmethod
    def prepare_message(message: str) -> Buffer:
        return message.encode("ascii")

    @staticmethod
    def validate_incoming_signature(
        incoming_signature: str,
        secret_key: bytes | bytearray | str,
        message: Buffer | str,
        algorithm=hashlib.sha256,
    ) -> bool:
        if isinstance(secret_key, str):
            secret_key = AuthenticationMethodHmac.prepare_secret(secret_key)

        if isinstance(message, str):
            message = AuthenticationMethodHmac.prepare_message(message)

        server_signature = AuthenticationMethodHmac.create_signature(
            secret_key, message, algorithm
        )

        return hmac.compare_digest(server_signature, incoming_signature)

    @staticmethod
    def create_signature(
        secret_key: bytes | bytearray | str,
        message: Buffer | str,
        algorithm=hashlib.sha256,
    ) -> str:
        if isinstance(secret_key, str):
            secret_key = AuthenticationMethodHmac.prepare_secret(secret_key)

        if isinstance(message, str):
            message = AuthenticationMethodHmac.prepare_message(message)

        # .digest returns bytes. this function generates a signature and also casts it as a string
        return base64.b64encode(
            hmac.new(secret_key, message, algorithm).digest()
        ).decode()

    @staticmethod
    def split_hmac_header(header: str) -> str:
        if "HMAC " not in header:
            return ""

        return header.split(" ", 1)[1]

    @staticmethod
    def create_hmac_header(signature: str) -> str:
        return f"HMAC {signature}"


class HmacInfo:
    message: str
    secret: str

    def __init__(self, secret, message):
        self.secret = secret
        self.message = message

    def make_header(self):
        return AuthenticationMethodHmac.create_hmac_header(self.make_key())

    def make_key(self):
        return AuthenticationMethodHmac.create_signature(
            self.secret,
            self.message,
        )
