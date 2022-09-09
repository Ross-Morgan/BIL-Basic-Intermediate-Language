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


class ASMFile:
    def __init__(self, path: str):
        self.filepath = path
        self.file = open(self.filepath, "w+")

    def __del__(self):
        self.file.close()


class AbstractASMWriter(ABC):
    platform_writers: dict[str, Type[AbstractASMWriter]] = {}

    constant_lines: list[str]
    variable_lines: list[str]
    text_lines: list[str]

    def __init_subclass__(cls, platform: str | list[str]) -> None:
        if isinstance(platform, str):
            AbstractASMWriter.platform_writers[platform] = cls
        else:
            for plat_name in platform:
                AbstractASMWriter.platform_writers[plat_name] = cls

    @classmethod
    def parse_data(cls, data: Constant | Variable) -> str:
        print(data, type(data))

        if isinstance(data.value, str):
            return f"{data.name} dw {cls.parse_value(data.value)}"
        if isinstance(data.value, Iterable):
            parsed_values = [cls.parse_value(v) for v in data.value]
            return f"{data.name} dw {', '.join(parsed_values)}"
        return f"{data.name} dw {cls.parse_value(data.value)}"

    @classmethod
    def parse_value(cls, value: object) -> str:
        if isinstance(value, str):
            return f"'{value}'"
        return value

    @property
    @classmethod
    def supported_platforms(cls) -> list[str]:
        return list(cls.platform_writers)

    @abstractmethod
    def __init__(self, filename: str):
        pass

    @abstractmethod
    def write_constants(self, constants: Iterable[HasConstantValue]):
        pass

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
    def __init__(self, filename: str):
        self.file = ASMFile(filename)

        self.constant_lines = ["section .data"]
        self.variable_lines = ["section .bss"]
        self.text_lines = []

    def write_constants(self, constants: Iterable[HasConstantValue]):
        self.constant_lines.extend([f"  {const.value.name} equ {self.parse_value(const.value.value)}" for const in constants])

    def write_variables(self, variables: Iterable[HasVariableValue]):
        self.variable_lines.extend([f"  {var.value.name}: {self.parse_value(var.value.value)}" for var in variables])

    def change_mode(self, mode: Mode):
        return super().change_mode(mode)

    def output(self):
        return super().output()


def new_writer(filename: str, *, platform: str = sys.platform) -> AbstractASMWriter:
    """
    Writer factory, returning a platform-specific
    subclass of AbstractASMWriter
    """
    writer = AbstractASMWriter.platform_writers[platform]
    return writer(filename)
