from graphviz import Digraph
from ast_nodes import *

def add_nodes(dot, node, parent_id=None, counter=[0]):
    node_id = f"node{counter[0]}"
    counter[0] += 1

    label = type(node).__name__
    if isinstance(node, NumberNode):
        label += f"({node.value})"
    elif isinstance(node, VariableNode):
        label += f"({node.name})"
    elif isinstance(node, StringNode):
        label += f'"{node.value}"'
    elif isinstance(node, AssignNode):
        label += f"({node.op.value})"
    elif isinstance(node, BinaryOpNode) or isinstance(node, UnaryOpNode):
        label += f"({node.op.value})"
    elif isinstance(node, FunctionCallNode):
        label += f"({node.name})"

    dot.node(node_id, label)

    if parent_id is not None:
        dot.edge(parent_id, node_id)

    children = []
    if isinstance(node, AssignNode):
        children = [node.left, node.right]
    elif isinstance(node, BinaryOpNode):
        children = [node.left, node.right]
    elif isinstance(node, UnaryOpNode):
        children = [node.expr]
    elif isinstance(node, FunctionCallNode):
        children = node.args
    elif isinstance(node, CompoundNode):
        children = node.children
    elif isinstance(node, IfNode):
        children = [node.condition, node.body]
        if node.else_body:
            children.append(node.else_body)
    elif isinstance(node, WhileNode):
        children = [node.condition, node.body]
    elif isinstance(node, ForNode):
        children = [node.init, node.condition, node.update, node.body]

    for child in children:
        if child is not None:
            dot = add_nodes(dot, child, node_id, counter)

    return dot

def generate_ast_graph(ast, filename="ast"):
    dot = Digraph()
    dot = add_nodes(dot, ast)
    dot.render(filename, format='png', cleanup=True)
