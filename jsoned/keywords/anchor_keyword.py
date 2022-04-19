from jsoned.json_core import ApplicatorKeyword, JsonSchema
from jsoned.types.json_complex import JsonObject
from jsoned.types.json_type import JsonType

__all__ = ["AnchorKeyword"]


class AnchorKeyword(ApplicatorKeyword):
    key: str = "$anchor"

    def apply(self, document: JsonSchema, node: JsonObject) -> JsonType:
        document.anchors[str(node["$anchor"])] = node
        del node["$anchor"]

        return node
