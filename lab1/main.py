import random

class Grammar:
    def __init__(self):
        self.VN = {"S", "A", "B"} 
        self.VT = {"a", "b", "c"} 
        self.P = { 
            "S": ["aS", "bS", "cA"],
            "A": ["aB"],
            "B": ["aB", "bB", "c"]
        }
        self.start_symbol = "S"
    
    def generate_string(self):
        result = self.start_symbol
        while any(sym in self.VN for sym in result):
            for sym in self.VN:
                if sym in result:
                    replacement = random.choice(self.P[sym])
                    result = result.replace(sym, replacement, 1)
        return result
    
    def generate_strings(self, count=5):
        return [self.generate_string() for _ in range(count)]
    
    def to_finite_automaton(self):
        Q = {"S", "A", "B", "Final"} 
        Sigma = self.VT  
        delta = {
            ("S", "a"): "S",
            ("S", "b"): "S",
            ("S", "c"): "A",
            ("A", "a"): "B",
            ("B", "a"): "B",
            ("B", "b"): "B",
            ("B", "c"): "Final",
        }
        q0 = "S" 
        F = {"Final"} 
        return FiniteAutomaton(Q, Sigma, delta, q0, F)

class FiniteAutomaton:
    def __init__(self, Q, Sigma, delta, q0, F):
        self.Q = Q
        self.Sigma = Sigma
        self.delta = delta
        self.q0 = q0
        self.F = F
    
    def string_belongs(self, input_string):
        state = self.q0
        for char in input_string:
            if (state, char) in self.delta:
                state = self.delta[(state, char)]
            else:
                return False
        return state in self.F

if __name__ == "__main__":
    grammar = Grammar()
    generated_strings = grammar.generate_strings()
    print("Generated Strings:", generated_strings)
    
    fa = grammar.to_finite_automaton()
    test_strings = generated_strings + ["aaa", "ccc", "bac"]
    
    for s in test_strings:
        print(f"'{s}' belongs to language: {fa.string_belongs(s)}")