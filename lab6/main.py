from lexer import Lexer, tokenize
from parser import Parser
from ast_visualizer import visualize_ast

def main():
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
    
    tokens = tokenize(code)
    
    print("Tokens:")
    for token in tokens:
        print(f"  {token}")
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    print("\nAbstract Syntax Tree:")
    print(visualize_ast(ast))

if __name__ == "__main__":
    main()