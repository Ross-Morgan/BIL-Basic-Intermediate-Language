from lexer import Lexer
from parser import Parser
from writer import new_writer


def main():
    lexer = Lexer("project/sample/source.bil")

    tokens = list(lexer.make_tokens())

    parser = Parser(tokens)
    parser.parse()

    print(parser.constant_tokens)
    print(parser.variable_tokens)

    writer = new_writer("project/sample/output.asm", platform="linux")
    writer.write_constants(parser.constant_tokens)
    writer.write_variables(parser.variable_tokens)



if __name__ == "__main__":
    main()
