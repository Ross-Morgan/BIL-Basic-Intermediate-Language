from copy import deepcopy
from itertools import chain, cycle
from typing import Iterable, Iterator
from data import Constant, Mode, Reference, Variable

from tokens import Token, Tokens

TAB_WIDTH = 2

CONSTANTS_SEC_MARKER = "  constants:"
VARIABLES_SEC_MARKER = "  variables:"


def has_regular_indentation(lines: Iterable[str]) -> bool:
    lines = map(lambda s: s.rstrip(), lines)
    lines = map(lambda s: s.replace("\t", " " * TAB_WIDTH), lines)

    # Indentation level of each line
    levels = [len(line) - len(line.lstrip()) for line in lines]

    # TODO Single level indentation not allowed
    if 1 in levels:
        return False

    # Remove empty lines
    levels = list(filter(lambda level: level > 0, levels))

    # Get lowest indentation level
    lowest_level = min(levels)

    for level in levels:
        if (level / lowest_level) % 1 != 0:
            return False
    return True


def normalise_indentation(lines: Iterable[str], regular_level: int = 2) -> list[str]:  # noqa
    if not has_regular_indentation(deepcopy(lines)):
        raise ValueError("Lines must have regular indentation level to be regularised")  # noqa

    # Remove newline characters
    lines = list(map(lambda s: s.replace("\n", ""), lines))

    # Indentation level of each line
    levels = [len(line) - len(line.lstrip()) for line in lines]

    # Remove empty lines
    non_zero_levels = list(filter(lambda level: level > 0, levels))

    # Get lowest indentation level
    lowest_level = min(non_zero_levels)

    # Calculate normalised indentation
    for i, level in enumerate(levels):
        levels[i] = int((level / lowest_level) * regular_level)

    # Remove indentation from lines
    unindented_lines = map(lambda line: line.lstrip(), lines)
    reindented_lines = []

    # Concentrate normalised indentation with each line
    for i, line in enumerate(unindented_lines):
        print("".join([" " * levels[i], line]))
        reindented_lines.append("".join([" " * levels[i], line]))

    return reindented_lines


class Lexer:
    def __init__(self, filename: str) -> None:
        self.filelines = open(filename, "r").readlines()
        self.filelines = chain(self.filelines, cycle([None]))

        self.filename = filename

        self.line_number = 0
        self.indentation = 0

        self.current_line = None

        self.advance()

    def advance(self):
        self.line_number += 1
        self.current_line = next(self.filelines)

        if self.current_line is None:
            return

        self.current_line = self.current_line.replace("\n", "")

    def make_tokens(self) -> Iterator[Token]:
        while self.current_line is not None:
            if self.current_line == "symbols:":
                self.advance()
                lines = []

                while self.current_line.startswith("  ") or self.current_line == "":  # noqa
                    lines.append(self.current_line)
                    self.advance()

                yield from self.make_symbol_tokens(lines)

            if self.current_line == "entry:":
                self.advance()
                lines = []

                while self.current_line is not None:
                    lines.append(self.current_line)
                    self.advance()

                yield Token(Tokens.SEC_ENTRY_POINT)
                yield from self.make_entry_tokens(lines)

            else:
                break

    def make_symbol_tokens(self, lines: list[str]) -> Iterator[Token]:
        if CONSTANTS_SEC_MARKER not in lines:
            raise ValueError(f"`symbols:` section missing `{CONSTANTS_SEC_MARKER.strip()}` marker")  # noqa
        if VARIABLES_SEC_MARKER not in lines:
            raise ValueError(f"`symbols:` section missing `{VARIABLES_SEC_MARKER.strip()}` marker")  # noqa

        # Remove all empty lines
        lines = list(filter(bool, lines))

        const_lines = lines[:lines.index(VARIABLES_SEC_MARKER)]
        vari_lines = lines[lines.index(VARIABLES_SEC_MARKER):]

        const_lines.pop(0)
        vari_lines.pop(0)

        const_lines = list(map(lambda s: s.lstrip(), const_lines))
        vari_lines = list(map(lambda s: s.lstrip(), vari_lines))

        for const_expr in const_lines:
            split_value = const_expr.split(": ")
            split_value.append(None)

            name = split_value.pop(0)
            value = split_value.pop(0)
            value = self.parse_value(value)

            if value is None:
                raise ValueError(f"Constant {name} must have value")

            yield Token(Tokens.DAT_CONSTANT, Constant(name, value))

        for vari_expr in vari_lines:
            split_value = vari_expr.split(": ")
            split_value.append(None)

            name = split_value.pop(0)
            value = split_value.pop(0)
            value = self.parse_value(value)

            yield Token(Tokens.DAT_VARIABLE, Variable(name, value))

    def make_entry_tokens(self, lines: list[str]):
        lines = list(map(lambda s: s[2:], lines))

        for line in lines:
            parts = line.split()

            if len(parts) == 1:
                command = parts[0]

                if command == "run":
                    yield Token(Tokens.KWD_RUN)

            if len(parts) == 2:
                command, arg = parts
                if command == "mode":
                    yield Token(Tokens.KWD_MODE, Mode(arg))
                if command == "load":
                    yield Token(Tokens.KWD_LOAD, self.parse_value(arg))

    def parse_value(self, value: str):
        if value is None:
            return None

        if value[0] == ":":
            return Reference(value[1:])

        # If wrapped in identical quotes
        if value[0] in "\"'" and value[-1] == value[0] and value[0] not in value[1: len(value) - 1]:  # noqa
            return value[1: len(value) - 1]

        if value[0] in "-0123456789":
            if "+" in value:
                x, y = map(str.strip, value.split("+"))
                x, y = map(self.parse_value, (x, y))

                return x + y

            if value[-1] == "i":
                return self.parse_value(value[:-1]) * 1j

            if "." in value:
                return float(value)
            return int(value)
        return value


def main():
    lexer = Lexer("project/sample/source.bil")
    tokens = list(lexer.make_tokens())

    print(*tokens, sep="\n")


if __name__ == "__main__":
    main()
