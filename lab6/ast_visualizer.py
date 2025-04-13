from ast_nodes import (
    NumberNode, VariableNode, BinaryOpNode, AssignNode, UnaryOpNode,
    FunctionCallNode, CompoundNode, IfNode, WhileNode, ForNode
)

# ast_visualizer.py
def visualize_ast(node, indent=""):
    if node is None:
        return indent + "None"
    
    result = indent + type(node).__name__
    
    if isinstance(node, NumberNode):
        result += f"({node.value})"
    elif isinstance(node, VariableNode):
        result += f"({node.name})"
    elif isinstance(node, BinaryOpNode) or isinstance(node, AssignNode):
        result += f"({node.op.value})\n"
        result += visualize_ast(node.left, indent + "    ") + "\n"
        result += visualize_ast(node.right, indent + "    ")
    elif isinstance(node, UnaryOpNode):
        result += f"({node.op.value})\n"
        result += visualize_ast(node.expr, indent + "    ")
    elif isinstance(node, FunctionCallNode):
        result += f"({node.name})\n"
        for i, arg in enumerate(node.args):
            result += visualize_ast(arg, indent + "    ")
            if i < len(node.args) - 1:
                result += "\n"
    elif isinstance(node, CompoundNode):
        result += "\n"
        for i, child in enumerate(node.children):
            result += visualize_ast(child, indent + "    ")
            if i < len(node.children) - 1:
                result += "\n"
    elif isinstance(node, IfNode):
        result += "\n"
        result += indent + "    Condition:\n"
        result += visualize_ast(node.condition, indent + "        ") + "\n"
        result += indent + "    Body:\n"
        result += visualize_ast(node.body, indent + "        ")
        if node.else_body:
            result += "\n" + indent + "    Else:\n"
            result += visualize_ast(node.else_body, indent + "        ")
    elif isinstance(node, WhileNode):
        result += "\n"
        result += indent + "    Condition:\n"
        result += visualize_ast(node.condition, indent + "        ") + "\n"
        result += indent + "    Body:\n"
        result += visualize_ast(node.body, indent + "        ")
    elif isinstance(node, ForNode):
        result += "\n"
        result += indent + "    Init:\n"
        result += visualize_ast(node.init, indent + "        ") + "\n"
        result += indent + "    Condition:\n"
        result += visualize_ast(node.condition, indent + "        ") + "\n"
        result += indent + "    Update:\n"
        result += visualize_ast(node.update, indent + "        ") + "\n"
        result += indent + "    Body:\n"
        result += visualize_ast(node.body, indent + "        ")
    
    return result