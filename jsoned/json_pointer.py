import re
from typing import Sequence, overload, List

__all__ = ["JsonPointer"]


class JsonPointer(Sequence[str]):
    POINTER_REGEX = re.compile(r"^(/(([^/~])|(~[01]))*)*$")

    def __init__(self, pointer: str) -> None:
        if not self.POINTER_REGEX.fullmatch(pointer):
            raise ValueError(f"Expected valid json pointer, `{pointer}` given instead.")

        self._path = [self.unescape(value) for value in pointer.split("/")[1:]]

    @overload
    def __getitem__(self, index: int) -> str:
        ...

    @overload
    def __getitem__(self, index: slice) -> "JsonPointer":
        ...

    def __getitem__(self, index):
        if isinstance(index, int):
            return self._path[index]
        if isinstance(index, slice):
            instance = JsonPointer.__new__(JsonPointer)
            instance._path = self._path[index]
            return instance

        raise TypeError(f"Expected `int` or `slice`, got `{type(index)}`.")

    def __len__(self) -> int:
        return len(self._path)

    def __str__(self) -> str:
        if not self._path:
            return ""
        return "".join(["/" + self.escape(item) for item in self._path])

    def __iter__(self):
        return iter(self._path)

    @classmethod
    def from_list(cls, pointer: List[str]) -> "JsonPointer":
        instance = JsonPointer.__new__(JsonPointer)
        instance._path = [self.escape(value) for value in pointer]

        return instance

    @staticmethod
    def escape(value: str) -> str:
        return value.replace("~", "~0").replace("/", "~1")

    @staticmethod
    def unescape(value: str) -> str:
        return value.replace("~1", "/").replace("~0", "~")
