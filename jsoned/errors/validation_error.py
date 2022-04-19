from typing import Any, Dict

__all__ = ["ValidationError"]


class ValidationError(ValueError):
    code: str = "error"
    message: str = ""
    path: str = ""

    def __init__(self, *args, **kwargs: Any):
        for key, value in kwargs.items():
            if key in ("code", "message", "path") or key in self.__annotations__:
                setattr(self, key, value)

        if args:
            self.message = str(args[0])
            super().__init__(*args)
        else:
            super().__init__(str(self))

    def __bool__(self) -> bool:
        return False

    def __str__(self) -> str:
        message = f"Failed validation at `{self.path}`. {self.message}"
        return message.format(**self.__dict__)
