from jsoned.json_core import ApplicatorKeyword, JsonSchema
from jsoned.types.json_complex import JsonObject
from jsoned.types.json_type import JsonType

__all__ = ["AnchorKeyword"]


class AnchorKeyword(ApplicatorKeyword):
    key: str = "$anchor"

    def apply(self, document: JsonSchema, node: JsonObject) -> JsonType:
        # ignore $anchor in enum or in const
        if "enum" in node.path or "const" in node.path:
            return node

        document.anchors[str(node["$anchor"])] = node

        return node
