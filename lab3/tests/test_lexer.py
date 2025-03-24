import sys
import os
import unittest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer import (
    Lexer, tokenize, Token,
    TOKEN_INTEGER, TOKEN_FLOAT, TOKEN_PLUS, TOKEN_MINUS,
    TOKEN_MULTIPLY, TOKEN_DIVIDE, TOKEN_LPAREN, TOKEN_RPAREN,
    TOKEN_FUNCTION, TOKEN_COMMA, TOKEN_EOF,
    TOKEN_IDENTIFIER, TOKEN_ASSIGN, TOKEN_EQUAL, TOKEN_NOT_EQUAL,
    TOKEN_LESS_THAN, TOKEN_GREATER_THAN, TOKEN_LESS_EQUAL, TOKEN_GREATER_EQUAL,
    TOKEN_AND, TOKEN_OR, TOKEN_NOT, TOKEN_POWER, TOKEN_MODULO,
    TOKEN_IF, TOKEN_ELSE, TOKEN_WHILE, TOKEN_FOR,
    TOKEN_SEMICOLON, TOKEN_COLON, TOKEN_DOT,
    TOKEN_LBRACE, TOKEN_RBRACE, TOKEN_LBRACKET, TOKEN_RBRACKET
)



class TestLexer(unittest.TestCase):
    
    def test_simple_tokens(self):
        lexer = Lexer("+ - * /")
        tokens = tokenize("+ - * /")
        
        self.assertEqual(len(tokens), 4)
        self.assertEqual(tokens[0].type, TOKEN_PLUS)
        self.assertEqual(tokens[1].type, TOKEN_MINUS)
        self.assertEqual(tokens[2].type, TOKEN_MULTIPLY)
        self.assertEqual(tokens[3].type, TOKEN_DIVIDE)
    
    def test_numbers(self):
        tokens = tokenize("42 3.14")
        
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TOKEN_INTEGER)
        self.assertEqual(tokens[0].value, 42)
        self.assertEqual(tokens[1].type, TOKEN_FLOAT)
        self.assertEqual(tokens[1].value, 3.14)
    
    def test_function_and_parens(self):
        tokens = tokenize("sin(45)")
        
        self.assertEqual(len(tokens), 4)
        self.assertEqual(tokens[0].type, TOKEN_FUNCTION)
        self.assertEqual(tokens[0].value, "sin")
        self.assertEqual(tokens[1].type, TOKEN_LPAREN)
        self.assertEqual(tokens[2].type, TOKEN_INTEGER)
        self.assertEqual(tokens[3].type, TOKEN_RPAREN)
    
    def test_complex_expression(self):
        expression = "sin(45) + 3.14 * cos(90) / sqrt(2)"
        tokens = tokenize(expression)
        
        self.assertEqual(len(tokens), 16)

    
    def test_error_handling(self):
        with self.assertRaises(Exception):
            tokenize("sin(45) @ 3.14")  
    
    def test_advanced_tokens(self):
        code = "if (x <= 10) { y = x * 2; }"
        tokens = tokenize(code)

        expected_types = [
            TOKEN_IF, TOKEN_LPAREN, TOKEN_IDENTIFIER, TOKEN_LESS_EQUAL,
            TOKEN_INTEGER, TOKEN_RPAREN, TOKEN_LBRACE, TOKEN_IDENTIFIER,
            TOKEN_ASSIGN, TOKEN_IDENTIFIER, TOKEN_MULTIPLY, TOKEN_INTEGER,
            TOKEN_SEMICOLON, TOKEN_RBRACE
        ]

        self.assertEqual(len(tokens), len(expected_types))

        for i, token_type in enumerate(expected_types):
            self.assertEqual(tokens[i].type, token_type)

if __name__ == "__main__":
    unittest.main()