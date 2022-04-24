from .json_store import JsonStore
from .keywords.ref_keyword import RefKeyword
from .keywords.anchor_keyword import AnchorKeyword
from .keywords.id_keyword import IdKeyword
from .keywords.type_keyword import TypeKeyword
from .keywords.enum_keyword import EnumKeyword
from .keywords.exclusive_maximum_keyword import ExclusiveMaximumKeyword
from .keywords.exclusive_minimum_keyword import ExclusiveMinimumKeyword
from .keywords.format_keyword import FormatKeyword
from .keywords.max_length_keyword import MaximumLengthKeyword
from .keywords.maximum_keyword import MaximumKeyword
from .keywords.min_length_keyword import MinimumLengthKeyword
from .keywords.minimum_keyword import MinimumKeyword
from .keywords.multiple_of_keyword import MultipleOfKeyword
from .keywords.pattern_keyword import PatternKeyword
from .keywords.properties_keyword import PropertiesKeyword
from .keywords.pattern_properties_keyword import PatternPropertiesKeyword


CORE_VOCABULARY = [
    RefKeyword(JsonStore.default()),
    AnchorKeyword(),
    IdKeyword(JsonStore.default()),
]

VALIDATOR_VOCABULARY = [
    TypeKeyword(),
    EnumKeyword(),
    ExclusiveMaximumKeyword(),
    ExclusiveMinimumKeyword(),
    FormatKeyword(),
    MaximumLengthKeyword(),
    MaximumKeyword(),
    MinimumLengthKeyword(),
    MinimumKeyword(),
    MultipleOfKeyword(),
    PatternKeyword(),
    PropertiesKeyword(),
    PatternPropertiesKeyword(),
]

DRAFT_2020_12_VOCABULARY = CORE_VOCABULARY + VALIDATOR_VOCABULARY
