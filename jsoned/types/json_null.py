from .json_type import JsonType

__all__ = ["JsonNull"]


class JsonNull(JsonType):
    type = JsonType.NULL

    def __init__(self, _=None, parent: JsonType = None, key: str = ""):
        super().__init__(None, parent, key)
