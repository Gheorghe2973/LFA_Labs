# main.py
from lexer import Lexer, tokenize
from parser import Parser
from ast_visualizer import visualize_ast

def main():
    # Example code to parse
    code = """
    {
        a = 10;
        b = 20;
        
        if (a > b) {
            max = a;
        } else {
            max = b;
        }
        
        sum = 0;
        for (i = 1; i <= 100; i = i + 1) {
            sum = sum + i;
        }
        
        result = sin(45) + cos(30) * 2;
    }
    """
    
    # Tokenize the code
    tokens = tokenize(code)
    
    # Print tokens for debugging
    print("Tokens:")
    for token in tokens:
        print(f"  {token}")
    
    # Parse tokens into AST
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Print AST
    print("\nAbstract Syntax Tree:")
    print(visualize_ast(ast))

if __name__ == "__main__":
    main()