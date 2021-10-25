from functools import partial
from json import load as _load_json

from yaml import FullLoader as YamlFullLoader, load as load_yaml

from jsoned.json_uri import JsonUri
from jsoned.utils import AnyJsonType
from jsoned.uri_loader import URILoader

_load_yaml = partial(load_yaml, Loader=YamlFullLoader)

__all__ = ["FileLoader"]


class FileLoader(URILoader):
    LOADERS = {
        "yaml": _load_yaml,
        "yml": _load_yaml,
        "json": _load_json,
    }

    def __init__(self):
        self.store = {}

    def load(self, uri: JsonUri) -> AnyJsonType:
        if uri.scheme != "file":
            raise ValueError(
                f"Unsupported scheme `{uri.scheme}`, expected `file` scheme."
            )

        file = open(uri.path, mode="r")
        extension = file.name.split(".")[-1]
        if extension not in self.LOADERS:
            raise TypeError(
                f"Could not load resource from uri `{file.name}` - unsupported file type, expected yml or json."
            )

        self.store[uri.base_uri] = self.LOADERS[extension](file)  # type: ignore

        return self.store[uri.base_uri]
