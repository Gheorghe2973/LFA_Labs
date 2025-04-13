# test_parser.py
import unittest
from lexer import tokenize
from parser import Parser
from ast_visualizer import visualize_ast
from ast_graphviz import generate_ast_graph
from ast_nodes import (
    NumberNode, VariableNode, BinaryOpNode, AssignNode, UnaryOpNode,
    FunctionCallNode, CompoundNode, IfNode, WhileNode, ForNode
)

class TestParser(unittest.TestCase):

    def test_simple_expression(self):
        tokens = tokenize("3 + 4 * 2")
        parser = Parser(tokens)
        ast = parser.parse()

        self.assertIsNotNone(ast)
        self.assertEqual(type(ast).__name__, "BinaryOpNode")
        self.assertEqual(ast.op.value, "+")
        self.assertEqual(type(ast.left).__name__, "NumberNode")
        self.assertEqual(ast.left.value, 3)
        self.assertEqual(type(ast.right).__name__, "BinaryOpNode")
        self.assertEqual(ast.right.op.value, "*")
        self.assertEqual(ast.right.left.value, 4)
        self.assertEqual(ast.right.right.value, 2)

    def test_function_call(self):
        tokens = tokenize("sin(45)")
        parser = Parser(tokens)
        ast = parser.parse()

        self.assertEqual(type(ast).__name__, "FunctionCallNode")
        self.assertEqual(ast.name, "sin")
        self.assertEqual(len(ast.args), 1)
        self.assertEqual(ast.args[0].value, 45)

    def test_assignment(self):
        tokens = tokenize("x = 10")
        parser = Parser(tokens)
        ast = parser.parse()

        self.assertEqual(type(ast).__name__, "AssignNode")
        self.assertEqual(ast.left.name, "x")
        self.assertEqual(ast.right.value, 10)

    def test_compound_statement(self):
        tokens = tokenize("{ x = 10; y = 20; }")
        parser = Parser(tokens)
        ast = parser.parse()

        self.assertEqual(type(ast).__name__, "CompoundNode")
        self.assertEqual(len(ast.children), 2)
        self.assertEqual(ast.children[0].left.name, "x")
        self.assertEqual(ast.children[1].left.name, "y")

    def test_if_statement(self):
        tokens = tokenize("if (x > 10) { y = 20; }")
        parser = Parser(tokens)
        ast = parser.parse()

        self.assertEqual(type(ast).__name__, "IfNode")
        self.assertEqual(type(ast.condition).__name__, "BinaryOpNode")
        self.assertEqual(ast.condition.op.value, ">")
        self.assertEqual(type(ast.body).__name__, "CompoundNode")
        self.assertEqual(ast.body.children[0].left.name, "y")

    def test_if_else_statement(self):
        tokens = tokenize("if (x > 10) { y = 20; } else { y = 30; }")
        parser = Parser(tokens)
        ast = parser.parse()

        self.assertEqual(type(ast).__name__, "IfNode")
        self.assertIsNotNone(ast.else_body)
        self.assertEqual(type(ast.else_body).__name__, "CompoundNode")
        self.assertEqual(ast.else_body.children[0].left.name, "y")

    def test_while_loop(self):
        tokens = tokenize("while (x < 10) { x = x + 1; }")
        parser = Parser(tokens)
        ast = parser.parse()

        self.assertEqual(type(ast).__name__, "WhileNode")
        self.assertEqual(type(ast.condition).__name__, "BinaryOpNode")
        self.assertEqual(ast.condition.op.value, "<")
        self.assertEqual(type(ast.body).__name__, "CompoundNode")

    def test_for_loop(self):
        tokens = tokenize("for (i = 0; i < 10; i = i + 1) { sum = sum + i; }")
        parser = Parser(tokens)
        ast = parser.parse()

        self.assertEqual(type(ast).__name__, "ForNode")
        self.assertEqual(ast.init.left.name, "i")
        self.assertEqual(ast.condition.op.value, "<")
        self.assertEqual(ast.update.left.name, "i")
        self.assertEqual(type(ast.body).__name__, "CompoundNode")

    def test_complex_expression(self):
        expr = "a = 5 * (3 + sin(45)) / 2"
        tokens = tokenize(expr)
        parser = Parser(tokens)
        ast = parser.parse()

        print("\nAST for expression:", expr)
        print(visualize_ast(ast))
        generate_ast_graph(ast, "ast_expression")  # ✅ Vizualizare

        self.assertEqual(type(ast).__name__, "AssignNode")
        self.assertEqual(ast.left.name, "a")
        self.assertEqual(type(ast.right).__name__, "BinaryOpNode")
        self.assertEqual(ast.right.op.value, "/")

    def test_complex_program(self):
        program = """
        {
            x = 0;
            sum = 0;
            while (x < 10) {
                sum = sum + x;
                x = x + 1;
            }
            if (sum > 50) {
                result = "High";
            } else {
                result = "Low";
            }
        }
        """
        tokens = tokenize(program)
        parser = Parser(tokens)
        ast = parser.parse()

        print("\nAST for program:")
        print(visualize_ast(ast))
        generate_ast_graph(ast, "ast_program")  # ✅ Vizualizare

        self.assertEqual(type(ast).__name__, "CompoundNode")
        self.assertEqual(len(ast.children), 4)


if __name__ == "__main__":
    unittest.main()
