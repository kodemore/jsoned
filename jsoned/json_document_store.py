from typing import Union, List

from .json_core import (
    JsonDocument,
    JsonDocumentStore as DocumentStoreProtocol,
    MetaJsonDocument,
)
from .json_uri import JsonUri
from .loaders.file_loader import FileLoader
from .uri_loader import URILoader


class JsonDocumentStore(DocumentStoreProtocol):
    _instance: DocumentStoreProtocol = None

    def __init__(self):
        self._loaders: Dict[str, URILoader] = {
            "file": FileLoader(),
        }
        self._store: Dict[str, JsonDocument] = {}

    def add(self, uri: JsonUri, json: JsonDocument) -> None:
        self._store[uri.base_uri] = json

    def add_loader(self, loader: URILoader, scheme: Union[str, List[str]]) -> None:
        if isinstance(scheme, str):
            scheme = [scheme]

        for s in scheme:
            self._loaders[s] = loader

    def load(self, uri: JsonUri, meta: MetaJsonDocument) -> JsonDocument:
        if uri.base_uri in self._store:
            return self._store[uri.base_uri]

        if uri.scheme not in self._loaders:
            raise ValueError(
                f"Unsupported scheme {uri.scheme}, please register scheme loader first."
            )

        document = JsonDocument(
            self._loaders[uri.scheme].load(uri), meta=meta, store=self
        )
        self.add(uri, document)

        return document

    @classmethod
    def default(cls) -> "JsonDocumentStore":
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance
