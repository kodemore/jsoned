from jsoned.utils import NoneType
from .json_type import JsonType

__all__ = ["JsonNull"]


class JsonNull(JsonType):
    type = "null"
