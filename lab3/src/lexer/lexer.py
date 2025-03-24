from .token import (
    Token, TOKEN_INTEGER, TOKEN_FLOAT, TOKEN_PLUS, TOKEN_MINUS,
    TOKEN_MULTIPLY, TOKEN_DIVIDE, TOKEN_LPAREN, TOKEN_RPAREN,
    TOKEN_FUNCTION, TOKEN_COMMA, TOKEN_EOF,
    TOKEN_IDENTIFIER, TOKEN_ASSIGN, TOKEN_EQUAL, TOKEN_NOT_EQUAL,
    TOKEN_LESS_THAN, TOKEN_GREATER_THAN, TOKEN_LESS_EQUAL, TOKEN_GREATER_EQUAL,
    TOKEN_AND, TOKEN_OR, TOKEN_NOT, TOKEN_POWER, TOKEN_MODULO,
    TOKEN_IF, TOKEN_ELSE, TOKEN_WHILE, TOKEN_FOR,
    TOKEN_SEMICOLON, TOKEN_COLON, TOKEN_DOT,
    TOKEN_LBRACE, TOKEN_RBRACE, TOKEN_LBRACKET, TOKEN_RBRACKET
)

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None
        self.functions = {'sin', 'cos', 'tan', 'log', 'sqrt'}
    
    def error(self):
        raise Exception(f'Invalid character: {self.current_char}')
    
    def advance(self):
        """Move to the next character in the input."""
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def peek(self):
        """Look at the next character without consuming it."""
        peek_pos = self.pos + 1
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]
    
    def skip_whitespace(self):
        """Skip spaces and tabs."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def number(self):
        """Parse a number from the input."""
        result = ''
        is_float = False
        
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if is_float:  
                    self.error()
                is_float = True
            result += self.current_char
            self.advance()
        
        if is_float:
            return Token(TOKEN_FLOAT, float(result))
        else:
            return Token(TOKEN_INTEGER, int(result))
    
    def identifier(self):
        """Handle identifiers and keywords."""
        result = ''
        
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        if result in self.functions:
            return Token(TOKEN_FUNCTION, result)
        
        if result.lower() == 'if':
            return Token(TOKEN_IF, result)
        elif result.lower() == 'else':
            return Token(TOKEN_ELSE, result)
        elif result.lower() == 'while':
            return Token(TOKEN_WHILE, result)
        elif result.lower() == 'for':
            return Token(TOKEN_FOR, result)
        elif result.lower() == 'and':
            return Token(TOKEN_AND, result)
        elif result.lower() == 'or':
            return Token(TOKEN_OR, result)
        elif result.lower() == 'not':
            return Token(TOKEN_NOT, result)
        
        # It's a regular identifier (variable name)
        return Token(TOKEN_IDENTIFIER, result)
    
    def get_next_token(self):
        """Lexical analyzer - breaks input into tokens."""
        while self.current_char is not None:
            
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char.isdigit() or self.current_char == '.':
                return self.number()
            
            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()
            
            if self.current_char == '=':
                if self.peek() == '=':
                    self.advance()  # consume first '='
                    self.advance()  # consume second '='
                    return Token(TOKEN_EQUAL, '==')
                else:
                    self.advance()
                    return Token(TOKEN_ASSIGN, '=')
                    
            if self.current_char == '!':
                if self.peek() == '=':
                    self.advance()  # consume '!'
                    self.advance()  # consume '='
                    return Token(TOKEN_NOT_EQUAL, '!=')
                else:
                    self.advance()
                    return Token(TOKEN_NOT, '!')
                    
            if self.current_char == '<':
                if self.peek() == '=':
                    self.advance()  # consume '<'
                    self.advance()  # consume '='
                    return Token(TOKEN_LESS_EQUAL, '<=')
                else:
                    self.advance()
                    return Token(TOKEN_LESS_THAN, '<')
                    
            if self.current_char == '>':
                if self.peek() == '=':
                    self.advance()  # consume '>'
                    self.advance()  # consume '='
                    return Token(TOKEN_GREATER_EQUAL, '>=')
                else:
                    self.advance()
                    return Token(TOKEN_GREATER_THAN, '>')
            
            # Single-character operators
            if self.current_char == '+':
                self.advance()
                return Token(TOKEN_PLUS, '+')
            
            if self.current_char == '-':
                self.advance()
                return Token(TOKEN_MINUS, '-')
            
            if self.current_char == '*':
                if self.peek() == '*':
                    self.advance()  # consume first '*'
                    self.advance()  # consume second '*'
                    return Token(TOKEN_POWER, '**')
                else:
                    self.advance()
                    return Token(TOKEN_MULTIPLY, '*')
            
            if self.current_char == '/':
                self.advance()
                return Token(TOKEN_DIVIDE, '/')
            
            if self.current_char == '^':
                self.advance()
                return Token(TOKEN_POWER, '^')
                
            if self.current_char == '%':
                self.advance()
                return Token(TOKEN_MODULO, '%')
            
            # Parentheses, braces, brackets
            if self.current_char == '(':
                self.advance()
                return Token(TOKEN_LPAREN, '(')
            
            if self.current_char == ')':
                self.advance()
                return Token(TOKEN_RPAREN, ')')
                
            if self.current_char == '{':
                self.advance()
                return Token(TOKEN_LBRACE, '{')
            
            if self.current_char == '}':
                self.advance()
                return Token(TOKEN_RBRACE, '}')
                
            if self.current_char == '[':
                self.advance()
                return Token(TOKEN_LBRACKET, '[')
            
            if self.current_char == ']':
                self.advance()
                return Token(TOKEN_RBRACKET, ']')
            
            # Other symbols
            if self.current_char == ',':
                self.advance()
                return Token(TOKEN_COMMA, ',')
                
            if self.current_char == ';':
                self.advance()
                return Token(TOKEN_SEMICOLON, ';')
                
            if self.current_char == ':':
                self.advance()
                return Token(TOKEN_COLON, ':')
                
            if self.current_char == '.':
                self.advance()
                return Token(TOKEN_DOT, '.')
            
            self.error()
        
        return Token(TOKEN_EOF, None)


def tokenize(text):
    """Utility function to convert text into a list of tokens."""
    lexer = Lexer(text)
    tokens = []
    token = lexer.get_next_token()
    
    while token.type != TOKEN_EOF:
        tokens.append(token)
        token = lexer.get_next_token()
    
    return tokens