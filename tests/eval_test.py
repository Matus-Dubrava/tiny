import pytest
from eval import Evaluator
from lexer import Lexer
from tiny_parser import Parser
import abstract_syntaxt_tree as ast
import object as obj
from environment import Environment


@pytest.mark.sanity
@pytest.mark.eval
def test_eval_integer_literal():
    input = "1"
    res = evaluate(input)
    assert_integer(res, 1)


@pytest.mark.sanity
@pytest.mark.eval
def test_eval_boolean_literal():
    input = "true"
    res = evaluate(input)
    assert_boolean(res, True)


@pytest.mark.sanity
@pytest.mark.eval
def test_eval_string_literal():
    input = '"Hello World"'
    res = evaluate(input)
    assert_string(res, "Hello World")


@pytest.mark.sanity
@pytest.mark.eval
def test_evaluate_prefix_expression():
    tests = [
        {"input": "!true", "expected": False},
        {"input": "!false", "expected": True},
        {"input": "!5", "expected": False},
        {"input": "!!true", "expected": True},
        {"input": "!!false", "expected": False},
        {"input": "!!5", "expected": True},
    ]

    for test in tests:
        res = evaluate(test["input"])
        print(f"{test['input']}, {res}")
        assert_boolean(res, test["expected"])


def evaluate(input: str) -> obj.Object:
    evaluator = Evaluator()
    env = Environment()
    lexer = Lexer(input)
    parser = Parser(lexer)
    program = parser.parse_program()
    return evaluator.eval(program, env)


def assert_integer(o: obj.Object, expected: int) -> None:
    assert isinstance(
        o, obj.IntegerObject
    ), f"expected 'IntegerObject', got '{o.__class__.__name__}'"
    assert o.value is expected, f"expected '{expected}', got '{o.value}'"


def assert_boolean(o: obj.Object, expected: bool) -> None:
    assert isinstance(
        o, obj.BooleanObject
    ), f"expected 'BooleanObject', got '{o.__class__.__name__}'"
    assert o.value is expected, f"expected '{expected}', got '{o.value}'"


def assert_string(o: obj.Object, expected: str) -> None:
    assert isinstance(
        o, obj.StringObject
    ), f"expected 'StringObject', got '{o.__class__.__name__}'"
    assert o.value == expected, f"expected '{expected}', got '{o.value}'"
