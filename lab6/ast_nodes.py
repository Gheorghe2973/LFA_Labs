class ASTNode:
    """Base class for all AST nodes"""
    pass

class BinaryOpNode(ASTNode):
    """Node representing a binary operation (e.g., +, -, *, /)"""
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right
    
    def __str__(self):
        return f"({self.left} {self.op.value} {self.right})"

class UnaryOpNode(ASTNode):
    """Node representing a unary operation (e.g., -, not)"""
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr
    
    def __str__(self):
        return f"{self.op.value}({self.expr})"

class NumberNode(ASTNode):
    """Node representing a numeric literal (integer or float)"""
    def __init__(self, token):
        self.token = token
        self.value = token.value
    
    def __str__(self):
        return str(self.value)

class VariableNode(ASTNode):
    """Node representing a variable reference"""
    def __init__(self, token):
        self.token = token
        self.name = token.value
    
    def __str__(self):
        return self.name

class AssignNode(ASTNode):
    """Node representing variable assignment"""
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right
    
    def __str__(self):
        return f"{self.left} {self.op.value} {self.right}"

class FunctionCallNode(ASTNode):
    """Node representing a function call"""
    def __init__(self, name_token, args=None):
        self.token = name_token
        self.name = name_token.value
        self.args = args if args else []
    
    def __str__(self):
        return f"{self.name}({', '.join(str(arg) for arg in self.args)})"

class CompoundNode(ASTNode):
    """Node representing a compound statement (block of code)"""
    def __init__(self, statements=None):
        self.children = statements if statements else []
    
    def __str__(self):
        return "{\n" + "\n".join([str(stmt) for stmt in self.children]) + "\n}"

class IfNode(ASTNode):
    """Node representing an if statement"""
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body
    
    def __str__(self):
        result = f"if ({self.condition}) {self.body}"
        if self.else_body:
            result += f" else {self.else_body}"
        return result

class WhileNode(ASTNode):
    """Node representing a while loop"""
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    
    def __str__(self):
        return f"while ({self.condition}) {self.body}"

class ForNode(ASTNode):
    """Node representing a for loop"""
    def __init__(self, init, condition, update, body):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body
    
    def __str__(self):
        return f"for ({self.init}; {self.condition}; {self.update}) {self.body}"

class NoOpNode(ASTNode):
    """Node representing a no-operation (empty statement)"""
    def __str__(self):
        return "NoOp"
    
class StringNode(ASTNode):
    """Node representing a string literal"""
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return f'"{self.value}"'
