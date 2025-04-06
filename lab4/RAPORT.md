# Laboratory Report: Custom Regex String Generator

## Course Info

- **Course**: Formal Languages & Finite Automata  
- **Laboratory**: 3rd  
- **Topic**: Custom Regex Parser & String Generator  
- **Author**: Cretu Dumitru  
- **Acknowledgment**: Cudos to Vasile Drumea and Irina Cojuhari  

---

## Overview

This lab explores the implementation of a **custom regular expression (regex) parser and string generator** in Python. Unlike full regex engines, this simplified parser focuses on a subset of regular expressions and dynamically generates valid strings that conform to the pattern.

Supported syntax elements include:
- Literal characters
- Groups and alternations (e.g., `(a|b)`)
- Repetition operators like `*`, `+`, and `^n`

The parser interprets the regex pattern, constructs valid combinations, and outputs both a random valid string and a list of all combinations (up to a limit). Additionally, it tracks the step-by-step parsing process.

---

## Objectives

- Understand what regular expressions are and their use in pattern matching and string processing.
- Interpret and evaluate simplified regular expressions dynamically.
- Generate valid strings that conform to given regex rules.
- Enforce a repetition limit for symbols with undefined repetitions (max 5 times).
- Track and display the sequence of operations applied during regex parsing (bonus).
- Document the process thoroughly and present results with traceability.

---

## Variant 4 Task

The assignment required implementing a solution for **Variant 4**, which involved interpreting and generating strings that match the following custom regex expressions:

![Variant 4 Regex Task](variant_4_task.png)

The patterns extracted and used from the image are:

1. `(S|T)(U|V)w*y+24`
2. `L(M|N)O^3P*Q(2|3)`
3. `R*S(T|U|V)W(x|y|z)^2`

Each pattern includes various elements of our supported syntax: grouping, alternation, repetition, and fixed substrings. The implementation was tailored specifically to handle this variant.

Expected sample outputs include:
- `{SUWWY24, SVWY24, ...}`
- `{LMOOOPPPQ2, LNOOOPQ3, ...}`
- `{RSTWXX, RRRSUWYY, ...}`

---

## Implementation Details

The project is implemented in **Python** and includes the following components:

### 1. `CustomRegexParser`
Main class responsible for parsing and generating strings.

#### Key Features:
- `parse(regex: str)` — generates one valid string by interpreting the regex.
- `generate_all_valid_combinations(regex: str)` — outputs multiple combinations for a pattern (with a configurable maximum).
- Handles custom repetition logic: `*` (zero or more), `+` (one repetition), and `^n` (exact n repetitions).
- Supports grouping with parentheses and alternation using `|`.
- Tracks internal processing steps via the `processing_steps` list.

#### Example Supported Patterns:
- `(a|b)c^3` → `accc` or `bccc`
- `x*y+z` → dynamically generated based on random repetition
- `L(M|N)O^3P*Q(2|3)` → complex nested parsing

### 2. `main()`
Entry point for testing the parser on multiple regex patterns. It:
- Initializes the parser
- Iterates over regex patterns
- Prints one valid string per pattern
- Prints a sample of all possible valid combinations (limited)
- Displays all recorded processing steps

### 3. Code Explanation

The code is structured around parsing a simplified regex grammar and generating strings accordingly. Here's a brief overview of how it works:

- **Grouping and Alternation:**
  ```python
  if regex[i] == '(':
      group_end = self._find_matching_parenthesis(regex, i)
      group_content = regex[i+1:group_end]  # Example: 'a|b'
      options = group_content.split('|')    # Result: ['a', 'b']
  ```
  This part extracts groups and handles alternation by splitting on the `|` symbol.

- **Repetition Operators:**
  ```python
  if regex[i+1] == '*':
      repetitions = random.randint(0, self.max_repetitions)
      string += char * repetitions
  elif regex[i+1] == '^' and regex[i+2].isdigit():
      repetitions = int(regex[i+2])
      string += char * repetitions
  elif regex[i+1] == '+':
      string += char  # Interpreted as one occurrence
  ```
  The code dynamically interprets how many times to repeat a character or group depending on the symbol used.

- **Recursive Combination Generation:**
  ```python
  def generate_combinations(parts_index=0, current=""):
      if parts_index >= len(parts):
          result.append(current)
          return
      ...  # Combines sub-results recursively based on part type
  ```
  This recursive function allows enumeration of all valid string combinations based on parsed parts.

---

## Example Usage

**Pattern:** `(S|T)(U|V)w*y+24`

**Possible Output:**
```plaintext
Random valid string: SUwyyy24
Sample of valid combinations:
  1. SU24
  2. SV24
  3. TU24
  4. TV24
  5. SUw24
```

**Processing Steps:**
```plaintext
1. Starting to parse custom regex: (S|T)(U|V)w*y+24
2. Processing group: S|T
3. Split alternation into options: ['S', 'T']
...
```

---

## Repository

The code will be hosted on a public GitHub repository (URL to be submitted on **ELSE**).

---

## Evaluation Notes

- Supports nested groups and alternations
- Custom repetition control is enforced (`^n`, `+`, `*`)
- Handles malformed patterns (e.g., unbalanced parentheses)
- Processing trace is useful for educational understanding
- Combinatorial explosion is mitigated with sampling logic
- Implementation fulfills all listed objectives from the assignment

---

## Conclusion

This lab introduced the construction of a lightweight regex parser that simulates the behavior of matching patterns by **generating valid strings**. It illustrates foundational concepts in **automata theory** and **formal languages** by enabling students to build and trace pattern evaluation.

The implementation is both functional and extensible, and the tracking of internal steps allows learners to follow the transformation from pattern to string. This approach promotes deeper understanding of how regex engines operate under the hood.

All requirements for **Variant 4** have been successfully met, including dynamic interpretation, repetition limits, traceability of parsing steps, and meaningful output samples. A public GitHub repository will be used for submission.

---

