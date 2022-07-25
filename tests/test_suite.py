import json
import pathlib

import pytest

from jsoned import JsonSchema
from jsoned.vocabulary import DRAFT_2020_12_VOCABULARY

schema_test_suits = pathlib.Path(__file__).parent / ".." / "json_test_suite" / "tests"

SKIP_TESTS = [
    # Refs and remote refs are working but those tests needs to be revisited and configured.
    "draft-2020 / ref.json / *",
    "draft-2020 / refRemote.json / *",
    "draft-2020 / dynamicRef.json / *",
    "draft-2020 / unknownKeyword.json / *",
    "draft-2020 / defs.json / *",

    "draft-2020 / id.json / *",

    # This is not right, 1.0 is not an integer
    "draft-2020 / type.json / integer type matches integers / a float with zero fractional part is an integer",

    # These formats are not supported
    "draft-2020 / format.json / uri-template format / *",

    # This behaviour should be revisited later on
    "draft-2020 / unevaluatedItems.json / unevaluatedItems with nested unevaluatedItems / with additional items",
    "draft-2020 / unevaluatedItems.json / unevaluatedItems with not / with unevaluated items",
    "draft-2020 / unevaluatedItems.json / unevaluatedItems can't see inside cousins / always fails",
    "draft-2020 / unevaluatedItems.json / unevaluatedItems depends on adjacent contains / second item is evaluated by contains",
    "draft-2020 / unevaluatedItems.json / unevaluatedItems depends on multiple nested contains / 5 not evaluated, passes unevaluatedItems",

]


def pytest_generate_tests(metafunc):
    parameters = []
    test_ids = []

    schema_suits = {
        "draft-2020": schema_test_suits / "draft2020-12",
    }

    for version, base_path in schema_suits.items():
        tests_files = sorted(base_path.glob("*.json"))

        for suite in tests_files:
            tests = json.load(open(suite))
            for section in tests:
                for test in section["tests"]:
                    test_id = f"{version} / {suite.name} / {section['description']} / {test['description']}"
                    skip = False
                    for pattern in SKIP_TESTS:
                        if not pattern.endswith("*"):
                            if test_id.replace(" ", "") == pattern.replace(" ", ""):
                                skip = True
                        else:
                            if test_id.replace(" ", "").startswith(pattern.replace(" ", "")[0:-1]):
                                skip = True
                    if skip:
                        continue
                    parameters.append(pytest.param(section["schema"], test["data"], test["valid"]))
                    test_ids.append(test_id)

    metafunc.parametrize(("schema", "data", "valid"), parameters, ids=test_ids)


def test_json_schema_suite(schema, data, valid):
    json_schema = JsonSchema(schema, vocabulary=DRAFT_2020_12_VOCABULARY)

    assert json_schema.validate(data) is valid
