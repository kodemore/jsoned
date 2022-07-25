from .json_store import JsonStore
from .keywords.additional_properties_keyword import AdditionalPropertiesKeyword
from .keywords.all_of_keyword import AllOfKeyword
from .keywords.anchor_keyword import AnchorKeyword
from .keywords.any_of_keyword import AnyOfKeyword
from .keywords.const_keyword import ConstKeyword
from .keywords.contains_keyword import ContainsKeyword
from .keywords.dependent_required_keyword import DependentRequiredKeyword
from .keywords.dependent_schemas_keyword import DependentSchemasKeyword
from .keywords.else_keyword import ElseKeyword
from .keywords.enum_keyword import EnumKeyword
from .keywords.exclusive_maximum_keyword import ExclusiveMaximumKeyword
from .keywords.exclusive_minimum_keyword import ExclusiveMinimumKeyword
from .keywords.format_keyword import FormatKeyword
from .keywords.id_keyword import IdKeyword
from .keywords.if_keyword import IfKeyword
from .keywords.items_keyword import ItemsKeyword
from .keywords.max_items_keyword import MaximumItemsKeyword
from .keywords.max_length_keyword import MaximumLengthKeyword
from .keywords.max_properties_keyword import MaximumPropertiesKeyword
from .keywords.maximum_keyword import MaximumKeyword
from .keywords.min_items_keyword import MinimumItemsKeyword
from .keywords.min_length_keyword import MinimumLengthKeyword
from .keywords.min_properties_keyword import MinimumPropertiesKeyword
from .keywords.minimum_keyword import MinimumKeyword
from .keywords.multiple_of_keyword import MultipleOfKeyword
from .keywords.not_keyword import NotKeyword
from .keywords.one_of_keyword import OneOfKeyword
from .keywords.pattern_keyword import PatternKeyword
from .keywords.pattern_properties_keyword import PatternPropertiesKeyword
from .keywords.prefix_items_keyword import PrefixItemsKeyword
from .keywords.properties_keyword import PropertiesKeyword
from .keywords.property_names_keyword import PropertyNamesKeyword
from .keywords.ref_keyword import RefKeyword
from .keywords.required_properties_keyword import RequiredPropertiesKeyword
from .keywords.then_keyword import ThenKeyword
from .keywords.type_keyword import TypeKeyword
from .keywords.unevaluated_items_keyword import UnevaluatedItemsKeyword
from .keywords.unevaluated_properties_keyword import UnevaluatedPropertiesKeyword
from .keywords.unique_items_keyword import UniqueItemsKeyword

CORE_VOCABULARY = [
    IdKeyword(JsonStore.default()),
    RefKeyword(JsonStore.default()),
    AnchorKeyword(),
]

COMPOSE_SCHEMA_VOCABULARY = [
    AllOfKeyword(),
    AnyOfKeyword(),
    ElseKeyword(),
    IfKeyword(),
    ThenKeyword(),
    NotKeyword(),
    OneOfKeyword(),
]

GENERIC_VALIDATORS_VOCABULARY = [
    TypeKeyword(),
    EnumKeyword(),
    ConstKeyword(),
]

NUMBER_VALIDATORS_VOCABULARY = [
    MinimumKeyword(),
    MaximumKeyword(),
    ExclusiveMaximumKeyword(),
    ExclusiveMinimumKeyword(),
    MultipleOfKeyword(),
]

STRING_VALIDATORS_VOCABULARY = [
    FormatKeyword(),
    MaximumLengthKeyword(),
    MinimumLengthKeyword(),
    PatternKeyword(),
]

OBJECT_VALIDATORS_VOCABULARY = [
    AdditionalPropertiesKeyword(),
    PropertiesKeyword(),
    PatternPropertiesKeyword(),
    RequiredPropertiesKeyword(),
    UnevaluatedPropertiesKeyword(),
    PropertyNamesKeyword(),
    DependentRequiredKeyword(),
    DependentSchemasKeyword(),
    MaximumPropertiesKeyword(),
    MinimumPropertiesKeyword(),
]

ARRAY_VALIDATORS_VOCABULARY = [
    ItemsKeyword(),
    PrefixItemsKeyword(),
    ContainsKeyword(),
    MinimumItemsKeyword(),
    MaximumItemsKeyword(),
    UniqueItemsKeyword(),
    UnevaluatedItemsKeyword(),
]

VALIDATORS_VOCABULARY = GENERIC_VALIDATORS_VOCABULARY + \
    NUMBER_VALIDATORS_VOCABULARY + \
    STRING_VALIDATORS_VOCABULARY + \
    OBJECT_VALIDATORS_VOCABULARY + \
    ARRAY_VALIDATORS_VOCABULARY


DRAFT_2020_12_VOCABULARY = CORE_VOCABULARY + VALIDATORS_VOCABULARY + COMPOSE_SCHEMA_VOCABULARY
