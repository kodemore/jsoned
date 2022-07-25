from functools import partial

from jsoned.json_core import JsonSchema, AssertionKeyword, can_apply_keyword
from jsoned.types.json_type import JsonType
from .composition_validators import validate_all
from .core_validators import Validator, ValidatorsMap, Context, fail_validation, pass_validation

_DEFERRED_VALIDATOR_CACHE = {}

__all__ = ["deferred_validator"]


def _build_validator(schema: JsonSchema, node: JsonType) -> Validator:
    rules = ValidatorsMap()
    if node.type == JsonType.BOOLEAN:
        if not node:
            return fail_validation
        return pass_validation

    if node.type != JsonType.OBJECT:
        return pass_validation

    for keyword in schema.vocabulary:
        if not isinstance(keyword, AssertionKeyword):
            continue

        if not can_apply_keyword(node, keyword):
            continue

        keyword.apply(schema, node, rules)

    return partial(validate_all, validators=rules)


def deferred_validator(value, context: Context, schema: JsonSchema, node: JsonType) -> bool:
    ref = str(schema.id) + str(node.path)
    if ref in _DEFERRED_VALIDATOR_CACHE:
        return _DEFERRED_VALIDATOR_CACHE[ref](value, context)

    if schema is None or node is None:
        return False

    _DEFERRED_VALIDATOR_CACHE[ref] = _build_validator(schema, node)

    return _DEFERRED_VALIDATOR_CACHE[ref](value, context)
