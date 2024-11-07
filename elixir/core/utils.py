import random
import re
import string
from urllib.parse import urljoin, urlparse

from flask import request, url_for
from werkzeug.routing import BuildError


def generate_id(length=8):
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
    return "".join(random.choices(alphabet, k=length))


def random_string(length=6):
    letters_and_digits = string.ascii_letters + string.digits
    return "".join(random.choice(letters_and_digits) for i in range(length))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


def string_to_list(s):
    # Use regular expression to split the string by
    # various separators and filter out empty strings
    return [item for item in re.split(r"[ ,;\n|]+", s.strip()) if item]


def is_valid_next_route(target):
    if target is None:
        return False

    if not is_safe_url(target):
        return False

    try:
        url_for(target)
        return True
    except BuildError:
        return False


def enum_coercer(enum_class):
    def _coerce(value):
        if isinstance(value, enum_class):
            return value
        try:
            return enum_class(int(value))
        except (ValueError, TypeError):
            raise ValueError(f"Invalid value {value} for enum {enum_class}")

    return _coerce


def true_false_empty(input_item: str):
    if input_item == "":
        return ""

    return input_item == "true"
