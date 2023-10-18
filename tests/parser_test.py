import pytest
from typing import Type

from tiny_parser import Parser
from lexer import Lexer
import abstract_syntaxt_tree as ast


@pytest.mark.sanity
@pytest.mark.parser
def test_parse_infix_expression():
    tests = [
        {"input": "!true;", "operator": "!", "expected_value": True},
        {"input": "!false", "operator": "!", "expected_value": False},
        {"input": "-1", "operator": "-", "expected_value": 1},
    ]

    for test in tests:
        lexer = Lexer(test["input"])
        parser = Parser(lexer)
        program = parser.parse_program()
        assert_no_parse_errors(parser)
        assert_program_length(program, 1)
        assert_node_type(program.statements[0], ast.PrefixExpression)

        if isinstance(test["expected_value"], bool):
            assert_boolean(program.statements[0].expr, test["expected_value"])
        elif isinstance(test["expected_value"], int):
            assert_integer(program.statements[0].expr, test["expected_value"])


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


def assert_integer(node: ast.Node, expected: int):
    assert isinstance(
        node, ast.IntegerLiteral
    ), f"expected 'IntegerLiteral', got '{node.__class__.__name__}'"
    assert node.value == expected


def assert_boolean(node: ast.Node, expected: int):
    assert isinstance(
        node, ast.BooleanLiteral
    ), f"expected 'BooleanLiteral', got '{node.__class__.__name__}'"
    assert node.value == expected
