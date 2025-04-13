# parser.py
from my_token import (
    Token, TOKEN_INTEGER, TOKEN_FLOAT, TOKEN_PLUS, TOKEN_MINUS,
    TOKEN_MULTIPLY, TOKEN_DIVIDE, TOKEN_LPAREN, TOKEN_RPAREN,
    TOKEN_FUNCTION, TOKEN_COMMA, TOKEN_EOF,
    TOKEN_IDENTIFIER, TOKEN_ASSIGN, TOKEN_EQUAL, TOKEN_NOT_EQUAL,
    TOKEN_LESS_THAN, TOKEN_GREATER_THAN, TOKEN_LESS_EQUAL, TOKEN_GREATER_EQUAL,
    TOKEN_AND, TOKEN_OR, TOKEN_NOT, TOKEN_POWER, TOKEN_MODULO,
    TOKEN_IF, TOKEN_ELSE, TOKEN_WHILE, TOKEN_FOR,
    TOKEN_SEMICOLON, TOKEN_COLON, TOKEN_DOT,
    TOKEN_LBRACE, TOKEN_RBRACE, TOKEN_LBRACKET, TOKEN_RBRACKET,
    TOKEN_STRING
)

from ast_nodes import (
    ASTNode, BinaryOpNode, UnaryOpNode, NumberNode, VariableNode, AssignNode,
    FunctionCallNode, CompoundNode, IfNode, WhileNode, ForNode, NoOpNode, StringNode  
)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = tokens[0] if tokens else None
    
    def error(self, expected=None):
        msg = f"Parser error at token: {self.current_token}"
        if expected:
            msg += f", expected: {expected}"
        raise Exception(msg)
    
    def eat(self, token_type):
        """Consume the current token if it matches the expected type."""
        if self.current_token.type == token_type:
            self.current_token_index += 1
            if self.current_token_index < len(self.tokens):
                self.current_token = self.tokens[self.current_token_index]
            else:
                self.current_token = Token(TOKEN_EOF, None)
        else:
            self.error(token_type)
    
    def program(self):
        """program : compound_statement"""
        node = self.compound_statement()
        return node
    
    def compound_statement(self):
        """compound_statement : '{' statement_list '}'"""
        if self.current_token.type == TOKEN_LBRACE:
            self.eat(TOKEN_LBRACE)
            nodes = self.statement_list()
            self.eat(TOKEN_RBRACE)
            return CompoundNode(nodes)
        else:
            # Allow single statements without braces
            return self.statement()
    
    def statement_list(self):
        """statement_list : (statement (';' | ε))*"""
        statements = []

        while self.current_token.type != TOKEN_RBRACE and self.current_token.type != TOKEN_EOF:
            stmt = self.statement()
            statements.append(stmt)
            if self.current_token.type == TOKEN_SEMICOLON:
                self.eat(TOKEN_SEMICOLON)

        return statements

    
    def statement(self):
        """
        statement : compound_statement
                  | assignment_statement
                  | if_statement
                  | while_statement
                  | for_statement
                  | expr
                  | empty
        """
        if self.current_token.type == TOKEN_LBRACE:
            return self.compound_statement()
        elif self.current_token.type == TOKEN_IDENTIFIER and self.peek_next_token().type == TOKEN_ASSIGN:
            return self.assignment_statement()
        elif self.current_token.type == TOKEN_IF:
            return self.if_statement()
        elif self.current_token.type == TOKEN_WHILE:
            return self.while_statement()
        elif self.current_token.type == TOKEN_FOR:
            return self.for_statement()
        elif self.current_token.type == TOKEN_SEMICOLON:
            self.eat(TOKEN_SEMICOLON)
            return NoOpNode()
        else:
            return self.expr()
    
    def assignment_statement(self):
        """assignment_statement : variable ASSIGN expr"""
        left = self.variable()
        token = self.current_token
        self.eat(TOKEN_ASSIGN)
        right = self.expr()
        return AssignNode(left, token, right)
    
    def if_statement(self):
        """if_statement : IF '(' expr ')' statement (ELSE statement)?"""
        self.eat(TOKEN_IF)
        self.eat(TOKEN_LPAREN)
        condition = self.expr()
        self.eat(TOKEN_RPAREN)
        
        if_body = self.statement()
        
        else_body = None
        if self.current_token.type == TOKEN_ELSE:
            self.eat(TOKEN_ELSE)
            else_body = self.statement()
        
        return IfNode(condition, if_body, else_body)
    
    def while_statement(self):
        """while_statement : WHILE '(' expr ')' statement"""
        self.eat(TOKEN_WHILE)
        self.eat(TOKEN_LPAREN)
        condition = self.expr()
        self.eat(TOKEN_RPAREN)
        body = self.statement()
        
        return WhileNode(condition, body)
    
    def for_statement(self):
        """for_statement : FOR '(' assignment_statement ';' expr ';' assignment_statement ')' statement"""
        self.eat(TOKEN_FOR)
        self.eat(TOKEN_LPAREN)
        
        init = self.assignment_statement()
        self.eat(TOKEN_SEMICOLON)
        
        condition = self.expr()
        self.eat(TOKEN_SEMICOLON)
        
        update = self.assignment_statement()
        self.eat(TOKEN_RPAREN)
        
        body = self.statement()
        
        return ForNode(init, condition, update, body)
    
    def variable(self):
        """variable : IDENTIFIER"""
        node = VariableNode(self.current_token)
        self.eat(TOKEN_IDENTIFIER)
        return node
    
    def empty(self):
        """empty :"""
        return NoOpNode()
    
    def expr(self):
        """expr : logical_expression"""
        return self.logical_expression()
    
    def logical_expression(self):
        """logical_expression : comparison_expression ((AND | OR) comparison_expression)*"""
        node = self.comparison_expression()
        
        while self.current_token.type in (TOKEN_AND, TOKEN_OR):
            token = self.current_token
            if token.type == TOKEN_AND:
                self.eat(TOKEN_AND)
            else:
                self.eat(TOKEN_OR)
            
            node = BinaryOpNode(node, token, self.comparison_expression())
        
        return node
    
    def comparison_expression(self):
        """
        comparison_expression : arithmetic_expression ((EQUAL | NOT_EQUAL | LESS_THAN | 
                                GREATER_THAN | LESS_EQUAL | GREATER_EQUAL) arithmetic_expression)*
        """
        node = self.arithmetic_expression()
        
        while self.current_token.type in (
            TOKEN_EQUAL, TOKEN_NOT_EQUAL, TOKEN_LESS_THAN, 
            TOKEN_GREATER_THAN, TOKEN_LESS_EQUAL, TOKEN_GREATER_EQUAL
        ):
            token = self.current_token
            if token.type == TOKEN_EQUAL:
                self.eat(TOKEN_EQUAL)
            elif token.type == TOKEN_NOT_EQUAL:
                self.eat(TOKEN_NOT_EQUAL)
            elif token.type == TOKEN_LESS_THAN:
                self.eat(TOKEN_LESS_THAN)
            elif token.type == TOKEN_GREATER_THAN:
                self.eat(TOKEN_GREATER_THAN)
            elif token.type == TOKEN_LESS_EQUAL:
                self.eat(TOKEN_LESS_EQUAL)
            elif token.type == TOKEN_GREATER_EQUAL:
                self.eat(TOKEN_GREATER_EQUAL)
            
            node = BinaryOpNode(node, token, self.arithmetic_expression())
        
        return node
    
    def arithmetic_expression(self):
        """arithmetic_expression : term ((PLUS | MINUS) term)*"""
        node = self.term()
        
        while self.current_token.type in (TOKEN_PLUS, TOKEN_MINUS):
            token = self.current_token
            if token.type == TOKEN_PLUS:
                self.eat(TOKEN_PLUS)
            else:
                self.eat(TOKEN_MINUS)
            
            node = BinaryOpNode(node, token, self.term())
        
        return node
    
    def term(self):
        """term : factor ((MULTIPLY | DIVIDE | MODULO) factor)*"""
        node = self.factor()
        
        while self.current_token.type in (TOKEN_MULTIPLY, TOKEN_DIVIDE, TOKEN_MODULO):
            token = self.current_token
            if token.type == TOKEN_MULTIPLY:
                self.eat(TOKEN_MULTIPLY)
            elif token.type == TOKEN_DIVIDE:
                self.eat(TOKEN_DIVIDE)
            else:
                self.eat(TOKEN_MODULO)
            
            node = BinaryOpNode(node, token, self.factor())
        
        return node
    
    def factor(self):
        """
        factor : PLUS factor
               | MINUS factor
               | NOT factor
               | INTEGER
               | FLOAT
               | LPAREN expr RPAREN
               | function_call
               | variable
               | power
        """
        token = self.current_token
        
        if token.type == TOKEN_PLUS:
            self.eat(TOKEN_PLUS)
            return UnaryOpNode(token, self.factor())
        elif token.type == TOKEN_MINUS:
            self.eat(TOKEN_MINUS)
            return UnaryOpNode(token, self.factor())
        elif token.type == TOKEN_NOT:
            self.eat(TOKEN_NOT)
            return UnaryOpNode(token, self.factor())
        elif token.type == TOKEN_INTEGER:
            self.eat(TOKEN_INTEGER)
            return NumberNode(token)
        elif token.type == TOKEN_FLOAT:
            self.eat(TOKEN_FLOAT)
            return NumberNode(token)
        elif token.type == TOKEN_LPAREN:
            self.eat(TOKEN_LPAREN)
            node = self.expr()
            self.eat(TOKEN_RPAREN)
            return node
        elif token.type == TOKEN_FUNCTION:
            return self.function_call()
        elif token.type == TOKEN_IDENTIFIER:
            return self.variable()
        elif token.type == TOKEN_STRING:
            self.eat(TOKEN_STRING)
            return StringNode(token)
        else:
            return self.power()
            
    
    def power(self):
        """power : atom (POWER factor)*"""
        node = self.atom()
        
        while self.current_token.type == TOKEN_POWER:
            token = self.current_token
            self.eat(TOKEN_POWER)
            node = BinaryOpNode(node, token, self.factor())
        
        return node
    
    def atom(self):
        """
        atom : INTEGER
             | FLOAT
             | LPAREN expr RPAREN
             | function_call
             | variable
        """
        token = self.current_token
        
        if token.type == TOKEN_INTEGER:
            self.eat(TOKEN_INTEGER)
            return NumberNode(token)
        elif token.type == TOKEN_FLOAT:
            self.eat(TOKEN_FLOAT)
            return NumberNode(token)
        elif token.type == TOKEN_LPAREN:
            self.eat(TOKEN_LPAREN)
            node = self.expr()
            self.eat(TOKEN_RPAREN)
            return node
        elif token.type == TOKEN_FUNCTION:
            return self.function_call()
        elif token.type == TOKEN_IDENTIFIER:
            return self.variable()
        else:
            self.error("INTEGER, FLOAT, LPAREN, FUNCTION or IDENTIFIER")
    
    def function_call(self):
        """function_call : FUNCTION LPAREN (expr (COMMA expr)*)? RPAREN"""
        token = self.current_token
        self.eat(TOKEN_FUNCTION)
        self.eat(TOKEN_LPAREN)
        
        args = []
        if self.current_token.type != TOKEN_RPAREN:
            args.append(self.expr())
            
            while self.current_token.type == TOKEN_COMMA:
                self.eat(TOKEN_COMMA)
                args.append(self.expr())
        
        self.eat(TOKEN_RPAREN)
        return FunctionCallNode(token, args)
    
    def peek_next_token(self):
        """Look at the next token without consuming the current one."""
        if self.current_token_index + 1 < len(self.tokens):
            return self.tokens[self.current_token_index + 1]
        return Token(TOKEN_EOF, None)
    
    def parse(self):
        """Parse the tokens and build an AST."""
        return self.program()
    
