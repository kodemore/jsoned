from abc import ABC, abstractmethod
from typing import List, Type

from .json_core import JsonDocument
from .types.json_type import JsonType


class Keyword(ABC):
    key: str
    dependencies: List["Keyword"]

    @staticmethod
    @abstractmethod
    def resolve(document: JsonDocument, node: JsonType) -> JsonType:
        ...


KeywordType = Type[Keyword]
