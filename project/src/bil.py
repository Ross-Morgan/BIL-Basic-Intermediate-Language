from lexer import Lexer
from parser import Parser


def main():
    lexer = Lexer("sample/source.bil")

    tokens = list(lexer.make_tokens())

    parser = Parser(tokens)
    parser.parse()


if __name__ == "__main__":
    main()
