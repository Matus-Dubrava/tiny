import abstract_syntaxt_tree as ast
import object as obj
from environment import Environment
from typing import Callable

DEBUG = True


def debug(eval_header: str):
    def wrapper(fn: Callable):
        def inner(*args, **kwargs):
            if DEBUG:
                print(
                    "".join(["\t"] * args[3]) + f" {eval_header} | node: {args[1]}",
                    end=None,
                )
            res = fn(*args, **kwargs)
            return res

        return inner

    return wrapper


def show_eval_info(depth: int, eval_name: str, node: ast.Node) -> None:
    if DEBUG:
        print("".join(["\t"] * depth) + f" {eval_name} | node: {node}")


class Evaluator:
    def eval(self, node: ast.Node, env: Environment, depth: int = 0) -> obj.Object:
        if isinstance(node, ast.Program):
            return self.eval_program(node, env, depth)
        if isinstance(node, ast.IntegerLiteral):
            return self.eval_integer_literal(node, env, depth)
        if isinstance(node, ast.BooleanLiteral):
            return self.eval_boolean_literal(node, env, depth)
        if isinstance(node, ast.StringLiteral):
            return self.eval_string_literal(node, env, depth)
        if isinstance(node, ast.PrefixExpression):
            return self.eval_prefix_expression(node, env, depth)
        if isinstance(node, ast.InfixExpression):
            return self.eval_infix_expression(node, env, depth)
        if isinstance(node, ast.IfExpression):
            return self.eval_if_expression(node, env, depth)
        if isinstance(node, ast.BlockStatement):
            return self.eval_block_statement(node, env, depth)
        if isinstance(node, ast.ReturnStatement):
            return self.eval_return_statement(node, env, depth)
        if isinstance(node, ast.LetStatement):
            return self.eval_let_statement(node, env, depth)
        if isinstance(node, ast.Identifier):
            return self.eval_identifier(node, env, depth)

    @debug("PROGRAM")
    def eval_program(self, program: ast.Program, env: Environment, depth: int):
        res_or_err: obj.Object = obj.NULL

        for stmt in program.statements:
            res_or_err = self.eval(stmt, env, depth)

            if isinstance(res_or_err, obj.ErrorObject):
                return res_or_err

            if isinstance(res_or_err, obj.ReturnObject):
                return res_or_err.value

        return res_or_err

    @debug("BLOCK STMT")
    def eval_block_statement(
        self, block: ast.BlockStatement, env: Environment, depth: int
    ) -> obj.Object:
        res_or_err: obj.Object = obj.NULL

        for stmt in block.statements:
            res_or_err = self.eval(stmt, env, depth)

            if isinstance(res_or_err, obj.ErrorObject) or isinstance(
                res_or_err, obj.ReturnObject
            ):
                return res_or_err

        return res_or_err

    @debug("RETURN")
    def eval_return_statement(
        self, return_stmt: ast.ReturnStatement, env: Environment, depth: int
    ) -> obj.Object:
        res = self.eval(return_stmt.expr, env, depth + 1)
        if isinstance(res, obj.ErrorObject):
            return res

        return obj.ReturnObject(res)

    @debug("LET")
    def eval_let_statement(
        self, let_stmt: ast.LetStatement, env: Environment, depth: int
    ) -> obj.Object:
        res = self.eval(let_stmt.expr, env, depth + 1)
        if isinstance(res, obj.ErrorObject):
            return res

        env.set(let_stmt.ident.name, res)

    @debug("IDENT")
    def eval_identifier(
        self, ident: ast.Identifier, env: Environment, depth: int
    ) -> obj.Object:
        return env.get(ident.name)

    @debug("IF EXPR")
    def eval_if_expression(
        self, if_expr: ast.IfExpression, env: Environment, depth: int
    ) -> obj.Object:
        cond = self.eval(if_expr.condition, env, depth + 1)
        if isinstance(cond, obj.ErrorObject):
            return cond

        if Evaluator.is_truthy(cond):
            return self.eval(if_expr.consequence, env, depth + 1)
        elif if_expr.alternative is not None:
            return self.eval(if_expr.alternative, env, depth + 1)
        else:
            return obj.NULL

    @debug("PREFIX")
    def eval_prefix_expression(
        self, prefix_expr: ast.PrefixExpression, env: Environment, depth: int
    ) -> obj.Object:
        left = self.eval(prefix_expr.expr, env, depth + 1)
        if isinstance(left, obj.ErrorObject):
            return left

        if prefix_expr.operator == "-":
            if isinstance(left, obj.IntegerObject):
                return obj.IntegerObject(-left.value)
            else:
                return obj.ErrorObject(
                    f"unrecognized operator '-', got '{left.__class__.__name__}'"
                )
        elif prefix_expr.operator == "!":
            if isinstance(left, obj.IntegerObject):
                if left.value == 0:
                    return obj.BooleanObject(True)
                else:
                    return obj.BooleanObject(False)
            elif isinstance(left, obj.BooleanObject):
                return obj.BooleanObject(not left.value)
        else:
            return obj.ErrorObject(
                f"unrecognized operator '-', got '{left.__class__.__name__}'"
            )

    @debug("INFIX")
    def eval_infix_expression(
        self, infix_expr: ast.InfixExpression, env: Environment, depth: int
    ) -> obj.Object:
        left = self.eval(infix_expr.left_expr, env, depth + 1)
        if isinstance(left, obj.ErrorObject):
            return left
        right = self.eval(infix_expr.right_expr, env, depth + 1)
        if isinstance(right, obj.ErrorObject):
            return right

        if left.__class__.__name__ != right.__class__.__name__:
            return obj.ErrorObject(
                f"type mismatch, got '{left.__class__.__name__}' and '{right.__class__.__name__}'"
            )

        if infix_expr.operator == "+":
            if isinstance(left, obj.IntegerObject):
                return obj.IntegerObject(left.value + right.value)
            elif isinstance(left, obj.StringObject):
                return obj.StringObject(left.value + right.value)
            else:
                return obj.ErrorObject(
                    f"unrecognized operator '-', got '{left.__class__.__name__}' and '{right.__class__.__name__}'"
                )
        elif infix_expr.operator == "-":
            if isinstance(left, obj.IntegerObject):
                return obj.IntegerObject(left.value - right.value)
            else:
                return obj.ErrorObject(
                    f"unrecognized operator '-', got '{left.__class__.__name__}' and '{right.__class__.__name__}'"
                )
        elif infix_expr.operator == "/":
            if isinstance(left, obj.IntegerObject):
                return obj.IntegerObject(left.value / right.value)
            else:
                return obj.ErrorObject(
                    f"unrecognized operator '/', got '{left.__class__.__name__}' and '{right.__class__.__name__}'"
                )
        elif infix_expr.operator == "*":
            if isinstance(left, obj.IntegerObject):
                return obj.IntegerObject(left.value * right.value)
            else:
                return obj.ErrorObject(
                    f"unrecognized operator '*', got '{left.__class__.__name__}' and '{right.__class__.__name__}'"
                )
        elif infix_expr.operator == "==":
            if (
                isinstance(left, obj.IntegerObject)
                or isinstance(left, obj.BooleanObject)
                or isinstance(left, obj.StringObject)
            ):
                return obj.BooleanObject(left.value == right.value)
            else:
                return obj.ErrorObject(
                    f"unrecognized operator '==', got '{left.__class__.__name__}' and '{right.__class__.__name__}'"
                )
        elif infix_expr.operator == "!=":
            if (
                isinstance(left, obj.IntegerObject)
                or isinstance(left, obj.BooleanObject)
                or isinstance(left, obj.StringObject)
            ):
                return obj.BooleanObject(left.value != right.value)
            else:
                return obj.ErrorObject(
                    f"unrecognized operator '!=', got '{left.__class__.__name__}' and '{right.__class__.__name__}'"
                )
        elif infix_expr.operator == "<":
            if isinstance(left, obj.IntegerObject):
                return obj.BooleanObject(left.value < right.value)
            else:
                return obj.ErrorObject(
                    f"unrecognized operator '<', got '{left.__class__.__name__}' and '{right.__class__.__name__}'"
                )
        elif infix_expr.operator == ">":
            if isinstance(left, obj.IntegerObject):
                return obj.BooleanObject(left.value > right.value)
            else:
                return obj.ErrorObject(
                    f"unrecognized operator '>', got '{left.__class__.__name__}' and '{right.__class__.__name__}'"
                )

    @debug("INTEGER")
    def eval_integer_literal(
        self, node: ast.IntegerLiteral, env: Environment, depth: int
    ) -> obj.Object:
        return obj.IntegerObject(node.value)

    @debug("BOOLEAN")
    def eval_boolean_literal(
        self, node: ast.BooleanLiteral, env: Environment, depth: int
    ) -> obj.Object:
        return obj.BooleanObject(node.value)

    @debug("STRING")
    def eval_string_literal(
        self, node: ast.StringLiteral, env: Environment, depth: int
    ) -> obj.Object:
        return obj.StringObject(node.value)

    @staticmethod
    def is_truthy(object: obj.Object):
        if isinstance(object, obj.BooleanObject) and object.value is True:
            return True
        elif isinstance(object, obj.IntegerObject) and object.value != 0:
            return True
        else:
            return False
