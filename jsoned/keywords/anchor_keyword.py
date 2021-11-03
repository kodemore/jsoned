from jsoned.json_core import Keyword, JsonDocument
from jsoned.types.json_object import JsonObject
from jsoned.types.json_type import JsonType

__all__ = ["AnchorKeyword"]


class AnchorKeyword(Keyword):
    key: str = "$anchor"

    def resolve(self, document: JsonDocument, node: JsonObject) -> JsonType:
        document.anchors[str(node["$anchor"])] = node

        return node
