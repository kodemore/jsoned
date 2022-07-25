from typing import Callable

from jsoned.validators.format_validators import (
    validate_format_boolean,
    validate_format_bytes,
    validate_format_date,
    validate_format_datetime,
    validate_format_decimal,
    validate_format_email,
    validate_format_hostname,
    validate_format_ip_address,
    validate_format_ip_address_v4,
    validate_format_ip_address_v6,
    validate_json_pointer,
    validate_format_pattern,
    validate_format_semver,
    validate_format_time,
    validate_format_time_duration,
    validate_format_uri,
    validate_format_iri,
    validate_format_iri_reference,
    validate_format_uri_reference,
    validate_format_url,
    validate_format_uuid,
)


__all__ = ["StringFormat"]


class _StringFormat:
    BOOLEAN = "boolean"
    BYTE = "byte"
    DATE = "date"
    DATE_TIME = "date-time"
    DECIMAL = "decimal"
    EMAIL = "email"
    HOSTNAME = "hostname"
    IP_ADDRESS = "ip-address"
    IP_ADDRESS_V4 = "ip-address-v4"
    IP_ADDRESS_V6 = "ip-address-v6"
    PATTERN = "pattern"
    SEMVER = "semver"
    TIME = "time"
    TIME_DURATION = "time-duration"
    DURATION = "duration"
    URI = "uri"
    URL = "url"
    IRI = "iri"
    IRI_REFERENCE = "iri-reference"
    URI_REFERENCE = "uri-reference"
    URI_TEMPLATE = "uri-template"
    UUID = "uuid"
    JSON_POINTER = "json-pointer"
    RELATIVE_JSON_POINTER = "relative-json-pointer"

    def __init__(self):
        self._formats = {
            self.BOOLEAN: validate_format_boolean,
            self.BYTE: validate_format_bytes,
            self.DATE: validate_format_date,
            self.DATE_TIME: validate_format_datetime,
            self.DECIMAL: validate_format_decimal,
            self.EMAIL: validate_format_email,
            "idn-email": validate_format_email,
            self.HOSTNAME: validate_format_hostname,
            "idn-hostname": validate_format_hostname,
            self.IP_ADDRESS: validate_format_ip_address,
            self.IP_ADDRESS_V4: validate_format_ip_address_v4,
            self.JSON_POINTER: validate_json_pointer,
            self.RELATIVE_JSON_POINTER: validate_json_pointer,
            "ipv4": validate_format_ip_address_v4,
            self.IP_ADDRESS_V6: validate_format_ip_address_v6,
            "ipv6": validate_format_ip_address_v6,
            self.PATTERN: validate_format_pattern,
            "regex": validate_format_pattern,
            self.SEMVER: validate_format_semver,
            self.TIME: validate_format_time,
            self.TIME_DURATION: validate_format_time_duration,
            self.DURATION: validate_format_time_duration,
            self.URI: validate_format_uri,
            self.URI_REFERENCE: validate_format_uri_reference,
            self.IRI: validate_format_iri,
            self.IRI_REFERENCE: validate_format_iri_reference,
            self.URL: validate_format_url,
            self.UUID: validate_format_uuid,
        }

    def __getitem__(self, format_name: str) -> Callable:
        if format_name in self._formats:
            return self._formats[format_name]
        raise KeyError(f"Unsupported format {format_name}")

    def __setitem__(self, format_name: str, value: Callable) -> None:
        self._formats[format_name] = value

    def __contains__(self, format_name: str) -> bool:
        return format_name in self._formats


StringFormat = _StringFormat()
