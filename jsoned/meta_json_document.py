from typing import List

from .json_core import JsonDocument, MetaJsonDocument as MetaJsonDocumentProtocol
from .keyword import KeywordType
from .keywords.ref_keyword import RefKeyword
from .types.json_type import JsonType
from .types.json_object import JsonObject
from .types.json_array import JsonArray


class MetaJsonDocument(MetaJsonDocumentProtocol):
    _instance: MetaJsonDocumentProtocol = None

    def __init__(self, keywords: List[KeywordType]):
        self._keywords: Set[KeywordType] = keywords

    def init(self, document: JsonDocument) -> None:
        document._value = self._init(document, document._value)

    def _init(self, document: JsonDocument, node: JsonType) -> JsonType:
        if not isinstance(node, (JsonObject, JsonArray)):
            return node

        if isinstance(node, JsonArray):
            for key, value in enumerate(node):
                node.value[key] = self._init(document, node[key])
            return node

        # iterate child documents first
        if isinstance(node, JsonObject):
            for key, value in node.items():
                node[key] = self._init(document, node[key])

        # process also the parent document
        for keyword in self._keywords:
            if keyword.key not in node:
                continue
            node = keyword.resolve(document, node)

        return node

    @classmethod
    def default(cls) -> "MetaJsonDocument":
        if cls._instance is None:
            cls._instance = cls([RefKeyword])

        return cls._instance
