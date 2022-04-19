import re
from typing import Sequence, overload, List

__all__ = ["JsonPointer"]


class JsonPointer(Sequence[str]):
    POINTER_REGEX = re.compile(r"^(/(([^/~])|(~[01]))*)*$")

    def __init__(self, pointer: str) -> None:
        if not self.POINTER_REGEX.fullmatch(pointer):
            raise ValueError(f"Expected valid json pointer, `{pointer}` given instead.")

        self._nodes = [self.unescape(value) for value in pointer.split("/")[1:]]

    def __contains__(self, item: str) -> bool:
        return item in self._nodes

    @overload
    def __getitem__(self, index: int) -> str:
        ...

    @overload
    def __getitem__(self, index: slice) -> "JsonPointer":
        ...

    def __getitem__(self, index):
        if isinstance(index, int):
            return self._nodes[index]
        if isinstance(index, slice):
            instance = JsonPointer.__new__(JsonPointer)
            instance._nodes = self._nodes[index]
            return instance

        raise TypeError(f"Expected `int` or `slice`, got `{type(index)}`.")

    def __len__(self) -> int:
        return len(self._nodes)

    def __str__(self) -> str:
        if not self._nodes:
            return "/"
        return "".join(["/" + self.escape(item) for item in self._nodes])

    def __iter__(self):
        return iter(self._nodes)

    @classmethod
    def from_list(cls, pointer: List[str]) -> "JsonPointer":
        instance = JsonPointer.__new__(JsonPointer)
        instance._nodes = pointer

        return instance

    @staticmethod
    def escape(value: str) -> str:
        return value.replace("~", "~0").replace("/", "~1")

    @staticmethod
    def unescape(value: str) -> str:
        return value.replace("~1", "/").replace("~0", "~")
