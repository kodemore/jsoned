from collections import Mapping

from jsoned.validators import ValidatorsMap


def test_can_instantiate() -> None:
    # given
    instance = ValidatorsMap[str]()

    # then
    assert isinstance(instance, ValidatorsMap)
    assert isinstance(instance, Mapping)


def test_can_add_item() -> None:
    # given
    instance = ValidatorsMap[str]()

    # when
    instance["a"] = lambda a, context: True

    # then
    assert "a" in instance


def test_can_iterate() -> None:
    # given
    instance = ValidatorsMap[str]()

    # when
    instance["a"] = 1
    instance["b"] = 2

    # then
    assert [i for i in instance] == [1, 2]

