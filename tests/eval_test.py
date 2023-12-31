import pytest
from eval import Evaluator
from lexer import Lexer
from tiny_parser import Parser
from object import Environment
import object as obj


@pytest.mark.sanity
@pytest.mark.eval
def test_eval_string_literal():
    input = '"Hello World"'
    res = evaluate(input)
    assert_string(res, "Hello World")


@pytest.mark.sanity
@pytest.mark.eval
def test_evaluate_string_concatenation():
    input = '"Hello" + " " + "World"'
    res = evaluate(input)
    assert_string(res, "Hello World")


@pytest.mark.sanity
@pytest.mark.eval
def test_evaluate_if_else_expression():
    tests = [
        {"input": "if (true) { 10 }", "expected": 10},
        {"input": "if (false) { 10 }", "expected": None},
        {"input": "if (1) { 10 }", "expected": 10},
        {"input": "if (1 < 2) { 10 }", "expected": 10},
        {"input": "if (1 > 2) { 10 }", "expected": None},
        {"input": "if (1 > 2) { 10 } else { 20 }", "expected": 20},
        {"input": "if (1 < 2) { 10 } else { 20 }", "expected": 10},
    ]

    for test in tests:
        res = evaluate(test["input"])
        if test["expected"] is None:
            assert res == obj.NULL
        else:
            assert_integer(res, test["expected"])


@pytest.mark.sanity
@pytest.mark.eval
def test_evaluate_integer_expression():
    tests = [
        {"input": "5", "expected": 5},
        {"input": "9999", "expected": 9999},
        {"input": "0", "expected": 0},
        {"input": "-1", "expected": -1},
        {"input": "-0", "expected": 0},
        {"input": "5 + 5 + 5 + 5 - 10", "expected": 10},
        {"input": "2 * 2 * 2 * 2 * 2", "expected": 32},
        {"input": "-50 + 100 + -50", "expected": 0},
        {"input": "5 * 2 + 10", "expected": 20},
        {"input": "5 + 2 * 10", "expected": 25},
        {"input": "20 + 2 * -10", "expected": 0},
        {"input": "50 / 2 * 2 + 10", "expected": 60},
        {"input": "2 * (5 + 10)", "expected": 30},
        {"input": "3 * 3 * 3 + 10", "expected": 37},
        {"input": "3 * (3 * 3) + 10", "expected": 37},
        {"input": "(5 + 10 * 2 + 15 / 3) * 2 + -10", "expected": 50},
    ]

    for test in tests:
        res = evaluate(test["input"])
        assert_integer(res, test["expected"])


@pytest.mark.sanity
@pytest.mark.eval
def test_evaluate_boolean_expression():
    tests = [
        {"input": "true", "expected": True},
        {"input": "false", "expected": False},
        {"input": "1 < 2", "expected": True},
        {"input": "1 > 2", "expected": False},
        {"input": "1 < 1", "expected": False},
        {"input": "1 > 1", "expected": False},
        {"input": "1 == 1", "expected": True},
        {"input": "1 != 1", "expected": False},
        {"input": "1 == 2", "expected": False},
        {"input": "1 != 2", "expected": True},
        {"input": "true == true", "expected": True},
        {"input": "true != true", "expected": False},
        {"input": "true != false", "expected": True},
        {"input": "true == false", "expected": False},
        {"input": "(1 < 2) == true", "expected": True},
        {"input": "(1 < 2) == false", "expected": False},
        {"input": "(1 > 2) == true", "expected": False},
        {"input": "(1 > 2) == false", "expected": True},
    ]

    for test in tests:
        res = evaluate(test["input"])
        assert_boolean(res, test["expected"])


@pytest.mark.sanity
@pytest.mark.eval
def test_evaluate_return_statement():
    tests = [
        {"input": "return 10;", "expected": 10},
        {"input": "return 10; 9;", "expected": 10},
        {"input": "return 2 * 5; 9;", "expected": 10},
        {"input": "9; return 2 * 5; 9;", "expected": 10},
        {
            "input": """ 
                if (10 > 1) {
                    if (10 > 1) {
                        return 10;
                    }
                    129
                    return 1;
                }""",
            "expected": 10,
        },
        {
            "input": """
                if (10 > 1) {
                    if (10 > 1) {
                        if (10 > 1) {
                            return 10;
                        }
                    }
                    129
                    return 1;
                }""",
            "expected": 10,
        },
    ]

    for test in tests:
        res = evaluate(test["input"])
        assert_integer(res, test["expected"])


@pytest.mark.sanity
@pytest.mark.eval
def test_evaluate_let_statement():
    tests = [
        {"input": "let a = 5; a;", "expected": 5},
        {"input": "let a = 5 * 5; a;", "expected": 25},
        {"input": "let a = 5; let b = a; b;", "expected": 5},
        {"input": "let a = 5; let b = a; let c = a + b + 5; c;", "expected": 15},
    ]

    for test in tests:
        res = evaluate(test["input"])
        assert_integer(res, test["expected"])


@pytest.mark.sanity
@pytest.mark.eval
def test_evaluate_function_expression():
    input = "fn(x) { x + 2 }"

    res = evaluate(input)
    assert isinstance(
        res, obj.FunctionObject
    ), f"expected 'FunctionObject', got '{res.__class__.__name__}'"
    assert len(res.arguments) == 1, f"expected '1' argument, got '{len(res.arguments)}'"
    assert (
        res.arguments[0].name == "x"
    ), f"expected arument 'x', got '{res.arguments[0].name}'"
    assert (
        f"{res.body.statements[0]}" == "(x + 2)"
    ), f"expected body '(x + 2)', got '{res.body.statements[0]}'"


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
    assert o.value == expected, f"expected '{expected}', got '{o.value}'"


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
