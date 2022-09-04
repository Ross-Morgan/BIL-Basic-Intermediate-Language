from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from typing import Iterable, Protocol, Type

from data import Constant, Mode, Variable
from tokens import Tokens


class HasConstantValue(Protocol):
    token_type: Tokens = Tokens.DAT_CONSTANT
    value: Constant


class HasVariableValue(Protocol):
    token_type: Tokens = Tokens.DAT_VARIABLE
    value: Variable


class AbstractASMWriter(ABC):
    platform_writers: dict[str, Type[AbstractASMWriter]] = {}

    def __init_subclass__(cls, platform: str | list[str]) -> None:
        if isinstance(platform, str):
            AbstractASMWriter.platform_writers[platform] = cls
        else:
            for plat_name in platform:
                AbstractASMWriter.platform_writers[plat_name] = cls

    @property
    @classmethod
    def supported_platforms(cls) -> list[str]:
        return list(cls.platform_writers)

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def write_constants(self, constants: Iterable[HasConstantValue]):
        for const in constants:
            const.value

    @abstractmethod
    def write_variables(self, variables: Iterable[HasVariableValue]):
        pass

    @abstractmethod
    def change_mode(self, mode: Mode):
        pass

    @abstractmethod
    def output(self):
        pass


class MacOSWriter(AbstractASMWriter, platform="darwin"):
    ...


class WindowsWriter(AbstractASMWriter, platform="win32"):
    ...


class LinuxWriter(AbstractASMWriter, platform=["linux", "linux2"]):
    def __init__(self):
        self.constant_lines = []
        self.variable_lines = []
        self.text_lines = []

    def write_constants(self, constants: Iterable[HasConstantValue]):
        lines = [f"  {const.value}" for const in constants]
        lines.insert(0, "section .data")


def new_writer(*, platform: str = sys.platform) -> AbstractASMWriter:
    """
    Writer factory, returning a platform-specific
    subclass of AbstractASMWriter
    """
    writer = AbstractASMWriter.platform_writers[platform]
    return writer()
