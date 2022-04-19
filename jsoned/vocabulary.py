from .json_store import JsonStore
from .keywords import RefKeyword, AnchorKeyword, IdKeyword


CORE_VOCABULARY = [
    RefKeyword(JsonStore.default()),
    AnchorKeyword(),
    IdKeyword(JsonStore.default()),
]
