from lexer import Lexer
from parser import Parser
from writer import new_writer


def main():
    lexer = Lexer("project/sample/source.bil")

    tokens = list(lexer.make_tokens())

    parser = Parser(tokens)
    parser.parse()

<<<<<<< HEAD
    print(parser.constant_tokens)
    print(parser.variable_tokens)
=======
    platform_writer = new_writer()
    writer = platform_writer()
>>>>>>> 49e39fd0a22e87caa0a2e9190798f1bb3cd3ecc2




if __name__ == "__main__":
    main()
