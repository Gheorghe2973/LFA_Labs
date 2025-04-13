class Grammar:
    def __init__(self, vn, vt, p, s):
        self.vn = vn
        self.vt = vt
        self.p = p
        self.s = s
        self.new_symbol_index = 0

    def get_new_symbol(self):
        while True:
            new_symbol = f"X{self.new_symbol_index}"
            self.new_symbol_index += 1
            if new_symbol not in self.vn:
                return new_symbol

    def remove_epsilon_productions(self):
        nullable = set()
        changed = True
        while changed:
            changed = False
            for lhs, rhs in self.p.items():
                if lhs in nullable:
                    continue
                for production in rhs:
                    if not production:
                        nullable.add(lhs)
                        changed = True
                        break
                    elif all(symbol in nullable for symbol in production):
                        nullable.add(lhs)
                        changed = True
                        break

        new_productions = {nt: [] for nt in self.p}
        for lhs, rhs_list in self.p.items():
            for rhs in rhs_list:
                if not rhs:
                    continue
                if rhs not in new_productions[lhs]:
                    new_productions[lhs].append(rhs)
                nullable_positions = [i for i, symbol in enumerate(rhs) if symbol in nullable]
                for mask in range(1, 2 ** len(nullable_positions)):
                    to_remove = []
                    for i, pos in enumerate(nullable_positions):
                        if (mask >> i) & 1:
                            to_remove.append(pos)
                    new_rhs = [symbol for i, symbol in enumerate(rhs) if i not in to_remove]
                    if new_rhs and new_rhs not in new_productions[lhs]:
                        new_productions[lhs].append(new_rhs)

        self.p = new_productions
        return self

    def remove_unit_productions(self):
        unit_pairs = {}
        for nt in self.vn:
            unit_pairs[nt] = {nt}
            changed = True
            while changed:
                changed = False
                for lhs, rhs_list in self.p.items():
                    if lhs == nt:
                        for rhs in rhs_list:
                            if len(rhs) == 1 and rhs[0] in self.vn and rhs[0] not in unit_pairs[nt]:
                                unit_pairs[nt].add(rhs[0])
                                changed = True

        new_productions = {nt: [] for nt in self.p}
        for lhs in self.vn:
            for nt in unit_pairs[lhs]:
                for rhs in self.p.get(nt, []):
                    if len(rhs) != 1 or rhs[0] not in self.vn:
                        if rhs not in new_productions[lhs]:
                            new_productions[lhs].append(rhs)

        self.p = new_productions
        return self

    def remove_inaccessible_symbols(self):
        accessible = {self.s}
        changed = True
        while changed:
            changed = False
            for lhs in list(accessible):
                for rhs in self.p.get(lhs, []):
                    for symbol in rhs:
                        if symbol in self.vn and symbol not in accessible:
                            accessible.add(symbol)
                            changed = True

        for nt in list(self.vn):
            if nt not in accessible:
                self.vn.remove(nt)
                if nt in self.p:
                    del self.p[nt]

        for lhs in list(self.p.keys()):
            if lhs not in self.vn:
                del self.p[lhs]
                continue
            self.p[lhs] = [rhs for rhs in self.p[lhs] if all(symbol in self.vn or symbol in self.vt for symbol in rhs)]

        return self

    def remove_non_productive_symbols(self):
        productive = set()
        changed = True
        while changed:
            changed = False
            for lhs, rhs_list in self.p.items():
                if lhs in productive:
                    continue
                for rhs in rhs_list:
                    if all(symbol in productive or symbol in self.vt for symbol in rhs):
                        productive.add(lhs)
                        changed = True
                        break

        for nt in list(self.vn):
            if nt not in productive:
                self.vn.remove(nt)
                if nt in self.p:
                    del self.p[nt]

        for lhs in list(self.p.keys()):
            if lhs not in self.vn:
                del self.p[lhs]
                continue
            self.p[lhs] = [rhs for rhs in self.p[lhs] if all(symbol in productive or symbol in self.vt for symbol in rhs)]

        return self

    def convert_to_cnf(self):
        terminal_productions = {}
        for t in self.vt:
            new_nt = self.get_new_symbol()
            self.vn.add(new_nt)
            self.p[new_nt] = [[t]]
            terminal_productions[t] = new_nt

        new_productions = {nt: [] for nt in self.vn}
        for lhs, rhs_list in self.p.items():
            for rhs in rhs_list:
                if len(rhs) == 1 and rhs[0] in self.vt:
                    new_productions[lhs].append(rhs)
                elif len(rhs) >= 2:
                    new_rhs = []
                    for symbol in rhs:
                        if symbol in self.vt:
                            new_rhs.append(terminal_productions[symbol])
                        else:
                            new_rhs.append(symbol)
                    while len(new_rhs) > 2:
                        new_nt = self.get_new_symbol()
                        self.vn.add(new_nt)
                        new_productions[new_nt] = [[new_rhs[-2], new_rhs[-1]]]
                        new_rhs = new_rhs[:-2] + [new_nt]
                    new_productions[lhs].append(new_rhs)

        self.p = new_productions
        return self

    def __str__(self):
        result = f"G = (VN, VT, P, {self.s})\n"
        result += f"VN = {self.vn}\n"
        result += f"VT = {self.vt}\n"
        result += "P = {\n"
        for lhs, rhs_list in self.p.items():
            for rhs in rhs_list:
                if rhs:
                    result += f"    {lhs} -> {''.join(rhs)}\n"
                else:
                    result += f"    {lhs} -> ε\n"
        result += "}"
        return result

def main():
    vn = {'S', 'A', 'B', 'C', 'D'}
    vt = {'a', 'b'}
    p = {
        'S': [['a', 'b', 'A', 'B']],
        'A': [['a', 'S', 'a', 'b'], ['B', 'S'], ['a', 'A'], ['b']],
        'B': [['B', 'A'], ['a', 'b', 'a', 'b', 'B'], ['b'], []],
        'C': [['A', 'S']],
        'D': []
    }
    s = 'S'
 
    grammar = Grammar(vn, vt, p, s)

    print("Original Grammar:")
    print(grammar)
    print("\nStep 1: After eliminating ε-productions")
    grammar.remove_epsilon_productions()
    print(grammar)

    print("\nStep 2: After eliminating unit productions (renaming)")
    grammar.remove_unit_productions()
    print(grammar)

    print("\nStep 3: After eliminating inaccessible symbols")
    grammar.remove_inaccessible_symbols()
    print(grammar)

    print("\nStep 4: After eliminating non-productive symbols")
    grammar.remove_non_productive_symbols()
    print(grammar)

    print("\nStep 5: Chomsky Normal Form")
    grammar.convert_to_cnf()
    print(grammar)

if __name__ == "__main__":
    main()
