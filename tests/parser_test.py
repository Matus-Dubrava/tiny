import pytest
from typing import Type

from tiny_parser import Parser
from lexer import Lexer
import abstract_syntaxt_tree as ast


@pytest.mark.sanity
@pytest.mark.parser
def test_operator_precendence():
    tests = [
        {"input": "-a * b", "expected": "((-a) * b)"},
        {"input": "!-a", "expected": "(!(-a))"},
        {"input": "a + b + c", "expected": "((a + b) + c)"},
        {"input": "a + b - c", "expected": "((a + b) - c)"},
        {"input": "a * b * c", "expected": "((a * b) * c)"},
        {"input": "a * b / c", "expected": "((a * b) / c)"},
        {"input": "a + b / c", "expected": "(a + (b / c))"},
        {
            "input": "a + b * c + d / e - f",
            "expected": "(((a + (b * c)) + (d / e)) - f)",
        },
        {"input": "3 + 4; -5 * 5", "expected": "(3 + 4); ((-5) * 5)"},
        {"input": "5 > 4 == 3 < 4", "expected": "((5 > 4) == (3 < 4))"},
        {"input": "5 < 4 != 3 > 4", "expected": "((5 < 4) != (3 > 4))"},
        {
            "input": "3 + 4 * 5 == 3 * 1 + 4 * 5",
            "expected": "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))",
        },
        {
            "input": "3 > 5 == false",
            "expected": "((3 > 5) == False)",
        },
        {
            "input": "3 < 5 == true",
            "expected": "((3 < 5) == True)",
        },
        {
            "input": "1 + (2 + 3) + 4",
            "expected": "((1 + (2 + 3)) + 4)",
        },
        {
            "input": "(5 + 5) * 2",
            "expected": "((5 + 5) * 2)",
        },
        {
            "input": "2 / (5 + 5)",
            "expected": "(2 / (5 + 5))",
        },
        {
            "input": "-(5 + 5)",
            "expected": "(-(5 + 5))",
        },
        {
            "input": "!(true == true)",
            "expected": "(!(True == True))",
        },
        # {
        #     "input": "a + add(b * c) + d",
        #     "expected": "((a + add((b * c))) + d)",
        # },
        # {
        #     "input": "add(a, b, 1, 2 * 3, 4 + 5, add(6, 7 * 8))",
        #     "expected": "add(a, b, 1, (2 * 3), (4 + 5), add(6, (7 * 8)))",
        # },
        # {
        #     "input": "add(a + b + c * d / f + g)",
        #     "expected": "add((((a + b) + ((c * d) / f)) + g))",
        # },
    ]

    for test in tests:
        lexer = Lexer(test["input"])
        parser = Parser(lexer)
        program = parser.parse_program()
        assert_no_parse_errors(parser)

        assert (
            f"{program}" == test["expected"]
        ), f'expected `{test["expected"]}`, got `{program}`'


@pytest.mark.sanity
@pytest.mark.parser
def test_parse_infix_expression():
    tests = [
        {
            "input": "5 + 5;",
            "expected_left": 5,
            "expected_operator": "+",
            "expected_right": 5,
        },
        {
            "input": "5 - 5;",
            "expected_left": 5,
            "expected_operator": "-",
            "expected_right": 5,
        },
        {
            "input": "5 * 5;",
            "expected_left": 5,
            "expected_operator": "*",
            "expected_right": 5,
        },
        {
            "input": "5 / 5;",
            "expected_left": 5,
            "expected_operator": "/",
            "expected_right": 5,
        },
        {
            "input": "5 > 5;",
            "expected_left": 5,
            "expected_operator": ">",
            "expected_right": 5,
        },
        {
            "input": "5 < 5;",
            "expected_left": 5,
            "expected_operator": "<",
            "expected_right": 5,
        },
        {
            "input": "5 == 5;",
            "expected_left": 5,
            "expected_operator": "==",
            "expected_right": 5,
        },
        {
            "input": "5 != 5;",
            "expected_left": 5,
            "expected_operator": "!=",
            "expected_right": 5,
        },
        {
            "input": "true == false;",
            "expected_left": True,
            "expected_operator": "==",
            "expected_right": False,
        },
        {
            "input": "true != false;",
            "expected_left": True,
            "expected_operator": "!=",
            "expected_right": False,
        },
    ]

    for test in tests:
        lexer = Lexer(test["input"])
        parser = Parser(lexer)
        program = parser.parse_program()
        assert_no_parse_errors(parser)
        assert_program_length(program, 1)

        assert_infix_expression(
            program.statements[0],
            test["expected_left"],
            test["expected_operator"],
            test["expected_right"],
        )


@pytest.mark.sanity
@pytest.mark.parser
def test_parse_prefix_expression():
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


@pytest.mark.sanity
@pytest.mark.parser
def test_parse_multiple_applications_of_prefix_express():
    tests = [
        {"input": "!!true;", "operator": "!", "expected_value": True},
        {"input": "!!false", "operator": "!", "expected_value": False},
        {"input": "--1", "operator": "-", "expected_value": 1},
    ]

    for test in tests:
        lexer = Lexer(test["input"])
        parser = Parser(lexer)
        program = parser.parse_program()
        assert_no_parse_errors(parser)
        assert_program_length(program, 1)
        assert_node_type(program.statements[0], ast.PrefixExpression)
        assert_node_type(program.statements[0].expr, ast.PrefixExpression)

        if isinstance(test["expected_value"], bool):
            assert_boolean(program.statements[0].expr.expr, test["expected_value"])
        elif isinstance(test["expected_value"], int):
            assert_integer(program.statements[0].expr.expr, test["expected_value"])


@pytest.mark.sanity
@pytest.mark.parser
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


def assert_boolean(node: ast.Node, expected: bool):
    assert isinstance(
        node, ast.BooleanLiteral
    ), f"expected 'BooleanLiteral', got '{node.__class__.__name__}'"
    assert node.value == expected


def assert_identifier(expr: ast.Node, expected: str):
    assert isinstance(expr, ast.Identifier)
    assert expr.name == expected, f"expected name '{expected}', got '{expr.name}'"


def assert_literal_expression(expr: ast.Node, expected: any):
    # This ugly condition is here because bool is actually instance of int
    # in Python. Without this, bools would be tested as int.
    if isinstance(expected, int) and expected != True and expected != False:
        assert_integer(expr, expected)
    elif isinstance(expected, bool):
        assert_boolean(expr, expected)
    elif isinstance(expected, str):
        assert_identifier(expr, expected)


def assert_infix_expression(
    expr: ast.Node, expected_left: any, operator: str, expected_right: any
):
    assert isinstance(expr, ast.InfixExpression)
    assert_literal_expression(expr.left_expr, expected_left)
    assert (
        operator == expr.operator
    ), f"expected operator '{operator}', got '{expr.operator}'"
    assert_literal_expression(expr.right_expr, expected_right)
