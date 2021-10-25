from hypothesis import strategies as fixture
from jsoned import JsonPointer

jsonpointer_fixture = fixture.from_regex(JsonPointer.POINTER_REGEX, fullmatch=True)
