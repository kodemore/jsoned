import base64
import re
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from ipaddress import AddressValueError, IPv4Address, IPv6Address
from typing import Any
from uuid import UUID

from jsoned.iso_datetime import (
    parse_iso_date,
    parse_iso_datetime,
    parse_iso_duration,
    parse_iso_time,
)

__all__ = [
    "validate_format_boolean",
    "validate_format_bytes",
    "validate_format_date",
    "validate_format_datetime",
    "validate_format_decimal",
    "validate_format_email",
    "validate_format_hostname",
    "validate_format_ip_address",
    "validate_format_ip_address_v4",
    "validate_format_ip_address_v6",
    "validate_format_pattern",
    "validate_format_semver",
    "validate_format_time",
    "validate_format_time_duration",
    "validate_format_uri",
    "validate_format_url",
    "validate_format_uuid",
]


def validate_format_pattern(value: Any) -> bool:
    try:
        re.compile(value)
        return True
    except Exception:
        return False


def validate_format_bytes(value: Any) -> bool:
    try:
        base64.b64decode(value)
        return True
    except Exception:
        return False


FALSY_EXPRESSION = {0, "0", "no", "n", "nope", "false", "f", "off"}
TRUTHY_EXPRESSION = {1, "1", "ok", "yes", "y", "yup", "true", "t", "on"}


def validate_format_boolean(value: Any) -> bool:
    if value in FALSY_EXPRESSION:
        return True

    if value in TRUTHY_EXPRESSION:
        return True

    return False


def validate_format_datetime(value: Any) -> bool:
    if isinstance(value, datetime):
        return True

    value = str(value)
    try:
        parse_iso_datetime(value)
        return True
    except ValueError:
        return False


def validate_format_date(value: Any) -> bool:
    if isinstance(value, date):
        return True

    value = str(value)
    try:
        parse_iso_date(value)
        return True
    except ValueError:
        return False


def validate_format_time(value: Any) -> bool:
    if isinstance(value, time):
        return True
    value = str(value)
    try:
        parse_iso_time(value)
        return True
    except ValueError:
        return False


def validate_format_time_duration(value: Any) -> bool:
    if isinstance(value, timedelta):
        return True

    value = str(value)
    try:
        parse_iso_duration(value)
        return True
    except Exception:
        return False


# https://www.w3.org/TR/html5/forms.html#valid-e-mail-address
EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+"
    r"@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$",
    re.I,
)


def validate_format_email(value: str) -> bool:
    """
    Keep in mind this validator willfully violates RFC 5322, the best way to invalidate email address is to send
    a message and receive confirmation from the recipient.
    """
    if not EMAIL_REGEX.match(value):
        return False
    if ".." in value:
        return False

    return True


HOSTNAME_REGEX = re.compile(
    r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[-0-9a-z]{0,61}[0-9a-z])?)*$",
    re.I,
)


def validate_format_hostname(value: str) -> bool:
    if not HOSTNAME_REGEX.match(value):
        return False

    return True


def validate_format_decimal(value: Any) -> bool:
    if isinstance(value, Decimal):
        return True

    try:
        value = Decimal(value)
        if not value.is_finite():
            return False

    except Exception:
        return False

    return True


def validate_format_ip_address_v4(value: Any) -> bool:
    try:
        IPv4Address(value)
        return True
    except AddressValueError:
        return False


def validate_format_ip_address_v6(value: Any) -> bool:
    try:
        IPv6Address(value)
        return True
    except AddressValueError:
        return False


def validate_format_ip_address(value: Any) -> bool:
    try:
        IPv4Address(value)
        return True
    except AddressValueError:
        try:
            IPv6Address(value)
            return True
        except AddressValueError:
            return False


SEMVER_REGEX = re.compile(
    r"^((([0-9]+)\.([0-9]+)\.([0-9]+)(?:-([0-9a-z-]+(?:\.[0-9a-z-]+)*))?)(?:\+([0-9a-z-]+(?:\.[0-9a-z-]+)*))?)$",
    re.I,
)


def validate_format_semver(value: Any) -> bool:
    value = str(value)
    if not SEMVER_REGEX.match(value):
        return False

    return True


URI_REGEX = re.compile(r"^(?:[a-z][a-z0-9+-.]*:)(?:\\/?\\/)?[^\s]*$", re.I)


def validate_format_uri(value: Any) -> bool:
    value = str(value)
    if not URI_REGEX.match(value):
        return False

    return True


URL_REGEX = re.compile(
    r"^(?:(?:https?|ftp):\/\/)(?:\S+(?::\S*)?@)?(?:(?!10(?:\.\d{1,3}){3})(?!127(?:\.\d{1,3}){3})(?!169\.254(?:\.\d{1,3}){2})(?!192\.168(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9_]+-?)*[a-z\u00a1-\uffff0-9_]+)(?:\.(?:[a-z\u00a1-\uffff0-9_]+-?)*[a-z\u00a1-\uffff0-9_]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/[^\s]*)?$",
    re.I | re.U,
)


def validate_format_url(value: Any) -> bool:
    value = str(value)
    if not URL_REGEX.match(value):
        return False

    return True


def validate_format_uuid(value: Any) -> bool:
    try:
        UUID(value)
        return True
    except Exception:
        return False
