from lexer import Lexer
from parser import Parser
from writer import new_writer


def main():
    lexer = Lexer("project/sample/source.bil")

    tokens = list(lexer.make_tokens())

    parser = Parser(tokens)
    parser.parse()

    writer = new_writer()

    writer.write_constants(parser.constant_tokens)
    writer.write_variables(parser.variable_tokens)

    print(writer.constant_lines)
    print(writer.variable_lines)


if __name__ == "__main__":
    main()
