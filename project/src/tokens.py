from dataclasses import dataclass, field
from enum import Enum, auto


@dataclass
class TokenMap:
    constants: dict[str, object] = field(default_factory=dict)
    variables: dict[str, object] = field(default_factory=dict)


class Tokens(Enum):
    SEC_SYMBOLS = auto()
    SEC_CONSTANTS = auto()
    SEC_VARIABLES = auto()
    SEC_ENTRY_POINT = auto()

    KWD_LOAD = auto()
    KWD_MODE = auto()
    KWD_RUN = auto()

    DAT_CONSTANT = auto()
    DAT_VARIABLE = auto()


@dataclass(repr=False, frozen=True)
class Token:
    token_type: Tokens
    value: object = None

    def __repr__(self) -> str:
        if self.value is not None:
            return f"<{self.token_type.name}: {self.value}>"
        return f"<{self.token_type.name}>"
