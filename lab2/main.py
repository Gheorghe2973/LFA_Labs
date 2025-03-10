class Grammar:
    def __init__(self, Vn, Vt, P, S):
        self.Vn = Vn
        self.Vt = Vt
        self.P = P
        self.S = S

    def classify_chomsky(self):
        is_type_3 = True
        is_type_2 = True
        is_type_1 = True

        for lhs, rhs_list in self.P.items():
            for rhs in rhs_list:
                if is_type_3:
                    right_linear = (len(rhs) <= 1 or 
                                   (len(rhs) == 2 and rhs[0] in self.Vt and rhs[1] in self.Vn))
                    left_linear = (len(rhs) <= 1 or 
                                  (len(rhs) == 2 and rhs[0] in self.Vn and rhs[1] in self.Vt))
                    if not (right_linear or left_linear):
                        is_type_3 = False

                if is_type_2 and (len(lhs) != 1 or lhs not in self.Vn):
                    is_type_2 = False

                if is_type_1:
                    if len(lhs) > len(rhs) and not (lhs == self.S and rhs == ''):
                        is_type_1 = False

        if is_type_3:
            return "Type 3: Regular Grammar"
        elif is_type_2:
            return "Type 2: Context-Free Grammar"
        elif is_type_1:
            return "Type 1: Context-Sensitive Grammar"
        else:
            return "Type 0: Unrestricted Grammar"


class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states

    def is_deterministic(self):
        defined_transitions = {}
        
        for (state, symbol), next_states in self.transitions.items():
            key = (state, symbol)
            
            if key in defined_transitions:
                return False
            defined_transitions[key] = True
            
            if isinstance(next_states, list) and len(next_states) > 1:
                return False
                
        return True

    def get_next_states(self, state, symbol):
        next_states = []
        for (s, sym), next_state in self.transitions.items():
            if s == state and sym == symbol:
                if isinstance(next_state, list):
                    next_states.extend(next_state)
                else:
                    next_states.append(next_state)
        return next_states

    def to_regular_grammar(self):
        Vn = self.states
        Vt = self.alphabet
        S = self.start_state
        
        P = {}
        for state in self.states:
            P[state] = []
            
        for (state, symbol), next_state in self.transitions.items():
            if isinstance(next_state, list):
                for ns in next_state:
                    if ns in self.final_states:
                        P[state].append(symbol)
                    P[state].append(symbol + ns)
            else:
                if next_state in self.final_states:
                    P[state].append(symbol)
                P[state].append(symbol + next_state)
        
        for final_state in self.final_states:
            if final_state in P:
                P[final_state].append('')
            else:
                P[final_state] = ['']
                
        return Grammar(Vn, Vt, P, S)

    def to_dfa(self):
        if self.is_deterministic():
            return self
            
        new_states = []
        new_transitions = {}
        new_final_states = []
        
        initial_state_set = frozenset([self.start_state])
        states_queue = [initial_state_set]
        new_states.append(initial_state_set)
        
        while states_queue:
            current_state_set = states_queue.pop(0)
            
            if any(state in self.final_states for state in current_state_set):
                new_final_states.append(current_state_set)
            
            for symbol in self.alphabet:
                next_state_set = set()
                
                for state in current_state_set:
                    next_states = self.get_next_states(state, symbol)
                    next_state_set.update(next_states)
                
                next_state_set = frozenset(next_state_set)
                
                if next_state_set:
                    new_transitions[(current_state_set, symbol)] = next_state_set
                    
                    if next_state_set not in new_states:
                        new_states.append(next_state_set)
                        states_queue.append(next_state_set)
        
        return FiniteAutomaton(
            states=new_states,
            alphabet=self.alphabet,
            transitions=new_transitions,
            start_state=initial_state_set,
            final_states=new_final_states
        )

    def visualize(self):
        dot_str = "digraph FiniteAutomaton {\n"
        dot_str += "    rankdir=LR;\n"
        dot_str += "    node [shape = circle];\n"
        
        for state in self.final_states:
            state_str = str(state).replace("'", "").replace(" ", "")
            dot_str += f'    "{state_str}" [shape = doublecircle];\n'
        
        dot_str += "    \"\" [shape=none,label=\"\"];\n"
        start_str = str(self.start_state).replace("'", "").replace(" ", "")
        dot_str += f'    "" -> "{start_str}";\n'
        
        for (state, symbol), next_states in self.transitions.items():
            if not isinstance(next_states, list):
                next_states = [next_states]
                
            state_str = str(state).replace("'", "").replace(" ", "")
            for next_state in next_states:
                next_state_str = str(next_state).replace("'", "").replace(" ", "")
                dot_str += f'    "{state_str}" -> "{next_state_str}" [label="{symbol}"];\n'
        
        dot_str += "}"
        return dot_str


def visualize_finite_automaton(dot_data, filename="finite_automaton"):
    try:
        import graphviz
        dot = graphviz.Source(dot_data)
        dot.render(filename, format="png", cleanup=True)
        print(f"Visualization saved as {filename}.png")
        dot.view()
    except ImportError:
        print("Warning: graphviz Python package not found. Visualization skipped.")
        print("Install it with: pip install graphviz")
        print("You'll also need the Graphviz software installed on your system.")
    except Exception as e:
        print(f"Error during visualization: {e}")
        print("Visualization skipped, but DOT data is available in the output.")


def main():
    states = {'q0', 'q1', 'q2', 'q3'}
    alphabet = {'a', 'b', 'c'}
    
    transitions = {
        ('q0', 'a'): ['q0', 'q1'],
        ('q1', 'b'): 'q2',
        ('q2', 'a'): 'q2',
        ('q2', 'b'): 'q3',
        ('q2', 'c'): 'q0'
    }
    
    start_state = 'q0'
    final_states = {'q3'}
    
    fa = FiniteAutomaton(states, alphabet, transitions, start_state, final_states)
    
    print("=== Analysis of Variant 15 Finite Automaton ===")
    
    is_det = fa.is_deterministic()
    print(f"\nIs the automaton deterministic? {is_det}")
    if not is_det:
        print("Reason: The transition δ(q0,a) has multiple destination states [q0, q1]")
    
    reg_grammar = fa.to_regular_grammar()
    print("\nConversion to Regular Grammar:")
    print(f"Non-terminals: {reg_grammar.Vn}")
    print(f"Terminals: {reg_grammar.Vt}")
    print("Productions:")
    for lhs, rhs_list in reg_grammar.P.items():
        rhs_str = " | ".join(rhs_list)
        print(f"{lhs} -> {rhs_str}")
    print(f"Start symbol: {reg_grammar.S}")
    
    grammar_type = reg_grammar.classify_chomsky()
    print(f"\nGrammar type: {grammar_type}")
    
    if not is_det:
        print("\nConverting NDFA to DFA:")
        dfa = fa.to_dfa()
        
        print("DFA States:")
        for state in dfa.states:
            state_str = ", ".join(state)
            print(f"State: {{{state_str}}}")
        
        print("\nDFA Transitions:")
        for (state, symbol), next_state in dfa.transitions.items():
            state_str = ", ".join(state)
            next_state_str = ", ".join(next_state)
            print(f"δ({{{state_str}}}, {symbol}) = {{{next_state_str}}}")
        
        print("\nDFA Start State:")
        start_state_str = ", ".join(dfa.start_state)
        print(f"{{{start_state_str}}}")
        
        print("\nDFA Final States:")
        for state in dfa.final_states:
            state_str = ", ".join(state)
            print(f"{{{state_str}}}")
        
        dfa_dot_data = dfa.visualize()
        print("\nDFA visualization data (can be used with Graphviz):")
        print(dfa_dot_data)
        
        visualize_finite_automaton(dfa_dot_data, "dfa_automaton")
    
    dot_data = fa.visualize()
    print("\nVisualization data for original NDFA (can be used with Graphviz):")
    print(dot_data)
    
    visualize_finite_automaton(dot_data, "ndfa_automaton")


if __name__ == "__main__":
    main()