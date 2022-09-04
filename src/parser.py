from typing import Iterable, Iterator

from tokens import Token, Tokens


class Parser:
    def __init__(self, tokens: Iterable[Token]):
        self.tokens = iter(tokens)

    def _get_tokens_by_type(self, token_type: Tokens) -> Iterator[Token]:  # noqa
        yield from filter(lambda t: t.token_type == token_type, self.tokens)

    def _get_tokens_by_value(self, value: object) -> Iterator[Token]:  # noqa
        yield from filter(lambda t: t.value == value, self.tokens)

    @property
    def constants(self) -> Iterator[Token]:
        yield from self._get_tokens_by_type(Tokens.DAT_CONSTANT)

    @property
    def variables(self) -> Iterator[Token]:
        yield from self._get_tokens_by_type(Tokens.DAT_VARIABLE)

    def parse(self):
        self.constant_tokens = list(self.constants)
        self.variable_tokens = list(self.variables)

        self.parse_entry()

    def parse_entry(self):
        pass
