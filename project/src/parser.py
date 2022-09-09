from typing import Iterable, Iterator

from data import Constant, ComplexReference, Variable
from tokens import Token, Tokens


class Parser:
    def __init__(self, tokens: Iterable[Token]):
        self.tokens = list(tokens)

    def _get_tokens_by_type(self, token_type: Tokens) -> list[Token]:
        return list(filter(lambda t: t.token_type == token_type, self.tokens))

    def _get_tokens_by_value(self, value: object) -> list[Token]:
        return list(filter(lambda t: t.value == value, self.tokens))

    @property
    def constants(self) -> list[Token]:
        return list(self._get_tokens_by_type(Tokens.DAT_CONSTANT))

    @property
    def variables(self) -> list[Token]:
        return list(self._get_tokens_by_type(Tokens.DAT_VARIABLE))

    def parse(self):
        self.tokens = self.parse_symbols()
        self.tokens = self.parse_entry()

        self.constant_tokens = list(self.constants)
        self.variable_tokens = list(self.variables)

    def parse_symbols(self):
        new_tokens: list[Token] = []
        tokens = list(self.tokens)

        type_map: dict[Tokens, Constant | Variable] = {
            Tokens.DAT_CONSTANT: Constant,
            Tokens.DAT_VARIABLE: Variable
        }

        for symbol_type, data_type in type_map.items():
            for i, token in enumerate(tokens):
                if token.token_type != symbol_type:
                    new_tokens.append(token)
                    continue

                if isinstance(token.value.value, complex):
                    re_name = f"re_{token.value.name}"
                    im_name = f"im_{token.value.name}"

                    ref_token = Token(symbol_type, ComplexReference(re_name, im_name))
                    re_token = Token(symbol_type, data_type(re_name, token.value.value))
                    im_token = Token(symbol_type, data_type(im_name, token.value.value))

                    new_tokens.extend([ref_token, re_token, im_token])

                    continue

                new_tokens.append(token)

        return new_tokens

    def parse_entry(self) -> list[Token]:
        return []
