import sys

from environment import Environment
from eval import Evaluator
from lexer import Lexer
from tiny_parser import Parser

if __name__ == "__main__":
    env = Environment()
    evaluator = Evaluator()

    while True:
        user_input = input(">> ")
        if user_input.lower() == "exit":
            sys.exit(0)

        lexer = Lexer(user_input)
        parser = Parser(lexer)
        program = parser.parse_program()

        if parser.errors:
            print(parser.errors)

        res = evaluator.eval(program, env)
        print(res)
