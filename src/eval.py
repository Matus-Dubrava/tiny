import abstract_syntaxt_tree as ast
import object as obj
from environment import Environment

DEBUG = True


def show_eval_info(depth: int, eval_name: str, node: ast.Node) -> None:
    if DEBUG:
        print("".join(["\t"] * depth) + f" {eval_name} | node: {node}")


class Evaluator:
    def eval(self, node: ast.Node, env: Environment, depth: int = 0) -> obj.Object:
        if isinstance(node, ast.Program):
            return self.eval_program(node, env, depth + 1)
        if isinstance(node, ast.IntegerLiteral):
            return self.eval_integer_literal(node, env, depth + 1)
        if isinstance(node, ast.BooleanLiteral):
            return self.eval_boolean_literal(node, env, depth + 1)
        if isinstance(node, ast.StringLiteral):
            return self.eval_string_literal(node, env, depth + 1)
        if isinstance(node, ast.PrefixExpression):
            return self.eval_prefix_expression(node, env, depth + 1)

    def eval_program(self, program: ast.Program, env: Environment, depth: int):
        show_eval_info(depth, "EVAL PROGRAM", program)

        res_or_err: obj.Object = obj.NULL

        for stmt in program.statements:
            res_or_err = self.eval(stmt, env, depth)
            if isinstance(res_or_err, obj.ErrorObject):
                return res_or_err

        return res_or_err

    def eval_prefix_expression(
        self, prefix_expr: ast.PrefixExpression, env: Environment, depth: int
    ) -> obj.Object:
        show_eval_info(depth, "EVAL INFIX", prefix_expr)

        left = self.eval(prefix_expr.expr, env, depth + 1)

        if prefix_expr.operator == "-":
            if isinstance(left, obj.IntegerObject):
                return obj.IntegerObject(-left)
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

    def eval_integer_literal(
        self, node: ast.IntegerLiteral, env: Environment, depth: int
    ) -> obj.Object:
        show_eval_info(depth, "EVAL INTEGER", node)
        return obj.IntegerObject(node.value)

    def eval_boolean_literal(
        self, node: ast.BooleanLiteral, env: Environment, depth: int
    ) -> obj.Object:
        show_eval_info(depth, "EVAL BOOLEAN", node)
        return obj.BooleanObject(node.value)

    def eval_string_literal(
        self, node: ast.StringLiteral, env: Environment, depth: int
    ) -> obj.Object:
        show_eval_info(depth, "EVAL STRING", node)
        return obj.StringObject(node.value)
