from abc import ABC, abstractmethod
from typing import Type

from .authentication_method import AuthenticationMethod
from .hmac_sig import AuthenticationMethodHmac

authentication_methods = {
    "hmac": AuthenticationMethodHmac
}


def determine_key_method(auth_header: str) -> tuple[any, str, Type[AuthenticationMethod]] | ValueError:
    method_name, value = auth_header.split(" ", 1)

    if method_name is None:
        return ValueError("Invalid header format. should be: `[method_name] [key]`")

    _authentication_method = authentication_methods.get(method_name, None)

    if _authentication_method is None:
        return ValueError("Invalid header format. should be: `[method_name] [key]`")

    return (
        method_name,
        value,
        _authentication_method
    )


def authenticate(auth_header: str) -> tuple[bool, str]:
    try:
        header_method_name, header_value, header_handler = determine_key_method(auth_header)

        return header_handler.handle_key(header_value)
    except ValueError as error:
        return (
            False,
            error.__str__()
        )
