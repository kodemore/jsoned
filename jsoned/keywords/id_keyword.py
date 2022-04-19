from typing import List, Tuple

from jsoned.json_core import ApplicatorKeyword, JsonSchema
from jsoned.json_store import JsonStore
from jsoned.types.json_complex import JsonObject
from jsoned.types.json_type import JsonType
from jsoned.uri import Uri

__all__ = ["IdKeyword"]


class IdKeyword(ApplicatorKeyword):
    key: List[str] = ["$id", "id"]

    def __init__(self, store: JsonStore):
        self._store = store

    def apply(self, schema: JsonSchema, node: JsonObject) -> JsonType:
        uri = Uri(str(node["$id"]) if "$id" in node else str(node["id"]))
        if uri.fragment:
            raise ValueError(f"`$id` cannot contain document fragment, `{uri.fragment}` found.")

        if node.is_root():  # id of the document
            schema.id = Uri(str(node["$id"]) if "$id" in node else str(node["id"]))
            if uri not in self._store:
                self._store.add(uri, schema)
            return node

        # ignore $ids in enum
        if "enum" in node.path:
            return node

        # the uri is not absolute, so we need to get the root's id
        if not uri.is_absolute:
            root_node: JsonObject = node.root

            # lets resolve uri by the root's node id
            if "$id" in root_node:
                base_uri = Uri(str(root_node["$id"]))
                uri = base_uri.resolve(uri)
            elif "id" in root_node:
                base_uri = Uri(str(root_node["id"]))
                uri = base_uri.resolve(uri)
            else:
                raise ValueError(f"Could not resolve base uri for `{uri}`. Please either provide absolute uri "
                                 f"or make sure `$id` node is present in your root node.")

        # Json allows to nest ids inside nodes which should create separate document,
        # this document is being stored in a global json store.
        child_document = JsonSchema(node, schema.vocabulary)
        child_document.id = uri
        self._store.add(uri, child_document)

        return node
