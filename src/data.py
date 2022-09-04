from dataclasses import dataclass
from enum import Enum


@dataclass
class Variable:
    name: str
    value: object


@dataclass
class Constant:
    name: str
    value: object


@dataclass
class Reference:
    ref_to: str


class Mode(Enum):
    PRINT = "print"
