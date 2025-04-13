
# Laboratory Report: Chomsky Normal Form Conversion

## Course Info

- **Course**: Formal Languages & Finite Automata  
- **Laboratory**: 5th  
- **Topic**: Chomsky Normal Form (CNF)  
- **Author**: Cretu Dumitru  
- **Acknowledgment**: Cudos to Vasile Drumea and Irina Cojuhari  

---

## Overview

This laboratory explores the transformation of a context-free grammar (CFG) into **Chomsky Normal Form** (CNF), an essential concept in formal languages and compiler design. CNF is a simplified representation that is particularly useful in syntax analysis and parsing algorithms.

The grammar transformation involves multiple steps:
1. Elimination of ε-productions (nullable rules).
2. Elimination of unit productions (renaming).
3. Removal of inaccessible symbols.
4. Elimination of non-productive symbols.
5. Final transformation into CNF.

---

## Objectives

- Understand and apply the step-by-step transformation process of CFG to CNF.
- Implement reusable methods for grammar normalization.
- Execute transformations on a specific grammar variant (Variant 16).
- Verify the final CNF grammar is correct and minimal.

---

## Variant 16 Task

We are given the following grammar:

```plaintext
G = (VN, VT, P, S)
VN = {S, A, B, C, D}
VT = {a, b}
P = {
    1.  S → abAB
    2.  A → aSab
    3.  A → BS
    4.  A → aA
    5.  A → b
    6.  B → BA
    7.  B → ababB
    8.  B → b
    9.  B → ε
    10. C → AS
}
```

We must apply transformations in the specified order to obtain CNF.

---

## Implementation Description

The implementation is encapsulated in a Python class called `Grammar`. The grammar transformation process is modularized into clearly defined steps, each corresponding to a normalization rule.

### Class: `Grammar`

- **Constructor**: Initializes the grammar with:
  - `VN`: Non-terminal symbols
  - `VT`: Terminal symbols
  - `P`: Production rules as a dictionary mapping non-terminals to RHS lists
  - `S`: Start symbol

---

### Key Methods

#### `remove_epsilon_productions()`
Identifies and eliminates productions that produce ε (empty string) by:
- Computing nullable symbols.
- Replacing ε-productions with adjusted alternatives that skip nullable symbols.

#### `remove_unit_productions()`
Removes renaming rules like `A → B` by:
- Identifying unit pairs (e.g., A derives B).
- Merging non-unit productions from all reachable units.

#### `remove_inaccessible_symbols()`
Eliminates symbols not reachable from the start symbol using a graph traversal approach.

#### `remove_non_productive_symbols()`
Removes symbols that do not lead to terminal derivations by:
- Detecting productive symbols.
- Cleaning up unproductive rules.

#### `convert_to_cnf()`
Transforms the remaining rules into CNF by:
- Replacing terminal symbols in long productions with new non-terminals.
- Ensuring all productions are of the form:
  - A → BC (two non-terminals)
  - A → a (single terminal)

#### Utility
- `get_new_symbol()`: Ensures new symbols don’t conflict with existing non-terminals.
- `__str__()`: Nicely prints the grammar.

---

## Execution & Output

The `main()` function defines the grammar from Variant 16 and applies transformations step by step. At each stage, intermediate grammars are printed:

```python
grammar.remove_epsilon_productions()
grammar.remove_unit_productions()
grammar.remove_inaccessible_symbols()
grammar.remove_non_productive_symbols()
grammar.convert_to_cnf()
```

Example final output format:
```plaintext
G = (VN, VT, P, S)
VN = {'S', 'A', 'B', ...}
VT = {'a', 'b'}
P = {
    S → AB
    A → XY
    ...
}
```

---

## Result Snapshot

After processing, the grammar will be:
- Free of ε-productions, unit productions.
- Contain only reachable, productive symbols.
- All productions will match CNF rules.

This transformation is both structurally and semantically equivalent to the original grammar.



## Conclusion

This lab provided a solid foundation in **CFG normalization** and **formal grammar manipulation**. By automating each stage, we ensured correctness and reusability of the CNF transformation. The results are immediately useful for further applications in syntax parsing, compiler construction, and theoretical CS studies.

---

## References

1. [Chomsky Normal Form – Wikipedia](https://en.wikipedia.org/wiki/Chomsky_normal_form)
