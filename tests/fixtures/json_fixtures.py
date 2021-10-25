from hypothesis import strategies as fixture

json_null_fixture = fixture.none()
json_string_fixture = fixture.text()

json_static_document_fixture = fixture.just(
    {
        "description": "an array of schemas for items",
        "schema": {"items": [{"type": "integer"}, {"type": "string"}]},
        "tests": [
            {"description": "correct types", "data": [1, "foo"], "valid": True},
            {
                "description": "array with additional items",
                "data": [1, "foo", True],
                "valid": True,
            },
        ],
    }
)
