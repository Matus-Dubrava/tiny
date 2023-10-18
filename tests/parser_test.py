import pytest
from typing import Dict, List, Type

from tiny_parser import Parser
from lexer import Lexer
import abstract_syntaxt_tree as ast


@pytest.mark.sanity
@pytest.mark.parser
def test_parse_infix_expression():
    pass


def test_parse_let_statement():
    tests = [
        {"input": "let a = 1;", "exp_n_statements": 1},
        {"input": "let other = 1 + 2", "exp_n_statements": 1},
        {"input": "let other = 1 + 2; let a = 1", "exp_n_statements": 2},
        {"input": "let other = 1 + 2; let a = 1; let b = true", "exp_n_statements": 3},
    ]

    for test in tests:
        lexer = Lexer(test["input"])
        parser = Parser(lexer)
        program = parser.parse_program()
        assert_no_parse_errors(parser)
        assert_program_length(program, test["exp_n_statements"])
        assert_node_type(program.statements[0], ast.LetStatement)


@pytest.mark.sanity
@pytest.mark.parser
def test_parse_return_statement():
    tests = [
        {"input": "return 1;", "exp_n_statements": 1},
        {"input": "return 1 + 2", "exp_n_statements": 1},
        {"input": "return 1 + 2; return 1", "exp_n_statements": 2},
        {"input": "return 1 + 2; return 1; return true", "exp_n_statements": 3},
    ]

    for test in tests:
        lexer = Lexer(test["input"])
        parser = Parser(lexer)
        program = parser.parse_program()
        assert_no_parse_errors(parser)
        assert_program_length(program, test["exp_n_statements"])
        assert_node_type(program.statements[0], ast.ReturnStatement)


def assert_no_parse_errors(parser: Parser):
    assert not parser.errors, f"expected no errors, got '{parser.errors}'"


def assert_program_length(program: ast.Program, expected_length: int):
    assert (
        len(program.statements) == expected_length
    ), f"expected '{expected_length}' stamtements, got '{len(program.statements)}'"


def assert_node_type(node: ast.Node, node_class: Type[ast.Node]):
    assert isinstance(
        node, node_class
    ), f"expected '{node.__class__.__name__}', got '{node_class.__name__}'"
