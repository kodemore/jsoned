from abc import abstractmethod
from typing import Protocol

from .json_uri import JsonUri
from .utils import AnyJsonType


class URILoader(Protocol):
    """
    Responsible for providing interface used to read
    and return file contents
    """

    @abstractmethod
    def load(self, uri: JsonUri) -> AnyJsonType:
        ...
