TOKEN_INTEGER = 'INTEGER'
TOKEN_FLOAT = 'FLOAT'
TOKEN_PLUS = 'PLUS'
TOKEN_MINUS = 'MINUS'
TOKEN_MULTIPLY = 'MULTIPLY'
TOKEN_DIVIDE = 'DIVIDE'
TOKEN_LPAREN = 'LPAREN'
TOKEN_RPAREN = 'RPAREN'
TOKEN_FUNCTION = 'FUNCTION'
TOKEN_COMMA = 'COMMA'
TOKEN_EOF = 'EOF'
TOKEN_IDENTIFIER = 'IDENTIFIER'
TOKEN_ASSIGN = 'ASSIGN'
TOKEN_EQUAL = 'EQUAL'
TOKEN_NOT_EQUAL = 'NOT_EQUAL'
TOKEN_LESS_THAN = 'LESS_THAN'
TOKEN_GREATER_THAN = 'GREATER_THAN'
TOKEN_LESS_EQUAL = 'LESS_EQUAL'
TOKEN_GREATER_EQUAL = 'GREATER_EQUAL'
TOKEN_AND = 'AND'
TOKEN_OR = 'OR'
TOKEN_NOT = 'NOT'
TOKEN_POWER = 'POWER'
TOKEN_MODULO = 'MODULO'
TOKEN_IF = 'IF'
TOKEN_ELSE = 'ELSE'
TOKEN_WHILE = 'WHILE'
TOKEN_FOR = 'FOR'
TOKEN_SEMICOLON = 'SEMICOLON'
TOKEN_COLON = 'COLON'
TOKEN_DOT = 'DOT'
TOKEN_LBRACE = 'LBRACE'
TOKEN_RBRACE = 'RBRACE'
TOKEN_LBRACKET = 'LBRACKET'
TOKEN_RBRACKET = 'RBRACKET'


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def __str__(self):
        return f"Token({self.type}, {self.value})"
    
    def __repr__(self):
        return self.__str__()