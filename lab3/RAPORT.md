
# Laboratory Report: Lexer & Scanner

## Course Info

- **Course**: Formal Languages & Finite Automata  
- **Laboratory**: 3rd  
- **Topic**: Lexer & Scanner  
- **Author**: Cretu Dumitru  
- **Acknowledgment**: Cudos to Vasile Drumea and Irina Cojuhari  

---

## Overview

The term **lexer** comes from *lexical analysis*, which is the process of converting a sequence of characters into a sequence of tokens. These tokens represent logical pieces of a language such as identifiers, operators, literals, and punctuation. Lexers are also known as **scanners** or **tokenizers**. They form an essential part of interpreters and compilers.

Tokens are not the same as lexemes. **Lexemes** are the actual substrings taken from the source text, whereas **tokens** represent the category to which a lexeme belongs.  
For example, the lexeme `3.14` might be classified as a token of type `FLOAT`.

---

## Objectives

- Understand the principles of lexical analysis.
- Learn how a lexer processes input.
- Implement a lexer that can tokenize mathematical expressions and control-flow keywords.

---

## Implementation Details

The project is implemented in **Python** and consists of the following modules:

### 1. `token.py`
Defines token types such as `INTEGER`, `FLOAT`, `PLUS`, `MINUS`, `IF`, `ELSE`, etc., and the `Token` class to represent each token as a type-value pair.

### 2. `lexer.py`
Implements the `Lexer` class which reads the input character-by-character and emits tokens. It handles:

- Integer and float numbers  
- Identifiers and keywords (`if`, `else`, `while`, `for`, `and`, `or`, `not`)  
- Mathematical functions like `sin`, `cos`, `tan`, `sqrt`, `log`  
- Operators (`+`, `-`, `*`, `/`, `%`, `==`, `!=`, `<=`, `>=`, etc.)  
- Punctuation (`(`, `)`, `{`, `}`, `[`, `]`, `,`, `;`, etc.)  

It includes support for **compound operators** and **error handling** for unexpected characters.

### 3. `__init__.py`
Provides re-exports for convenient importing of the lexer and tokens.

### 4. `test_lexer.py`
Contains a suite of unit tests using `unittest`. It tests:

- Simple token recognition  
- Number parsing (integers and floats)  
- Function recognition  
- Complex expressions  
- Error handling for invalid characters  
- Parsing of control flow structures  

---

## Example Usage

**Input:**

```plaintext
sin(45) + 3.14 * cos(90) / sqrt(2)
```

**Output Tokens:**

```plaintext
[FUNCTION(sin), LPAREN(()), INTEGER(45), RPAREN()), PLUS(+), FLOAT(3.14), MULTIPLY(*), FUNCTION(cos), LPAREN(()), INTEGER(90), RPAREN()), DIVIDE(/), FUNCTION(sqrt), LPAREN(()), INTEGER(2), RPAREN())]
```

---

## Repository

The code is hosted on a public Git repository (URL to be submitted on **ELSE**).

---

## Evaluation Notes

- Lexer supports both floats and integers.  
- Includes trigonometric functions.  
- Structure follows modular best practices.  
- Comprehensive test coverage.  

---

## Conclusion

This lab introduced the fundamental principles of **lexical analysis**, a core component in building interpreters and compilers. The implemented lexer is capable of identifying a wide range of tokens from mathematical and programming constructs. 

By extending the classic calculator example to include **floating point numbers** and **trigonometric functions**, the project meets the **enhanced complexity criteria**. The result is a versatile and well-tested lexical analyzer suitable for use in larger language processing projects.

---

## 🧠 More Explanation

### 🔍 Overview

Lexical analysis is the **first stage of compilation or interpretation**. It takes raw input (like what a user writes in code) and breaks it into **tokens**—basic building blocks such as:

- `if`, `else`, `while` → keywords  
- `3.14`, `42` → numbers  
- `+`, `-`, `==` → operators  
- `(`, `)` → punctuation  
- `sqrt`, `sin` → functions

These tokens help the compiler understand what the code is trying to do.

**Lexemes** are the actual pieces of text (like `3.14`), and **tokens** are their categories (like `FLOAT`).

---

### 🎯 Objectives

You're not just building a lexer—you’re learning:

- What lexers do in the bigger picture of a compiler/interpreter.
- How to write a program that mimics what professional tools like Python’s own lexer do.
- How to handle more than just basic math: you'll also parse keywords (`if`, `else`) and functions (`sin`, `cos`).

---

### ⚙️ Implementation Details

You split the logic into several Python modules, each with a clear role:

#### `token.py`
Defines **token types** (like `PLUS`, `FLOAT`, `IF`) and a `Token` class that holds:
- the token's **type**
- the **value** it represents

For example, `Token("FLOAT", 3.14)`.

#### `lexer.py`
This is the **core of the project**. It reads characters one-by-one and groups them into tokens.

It can detect:
- Numbers (int and float)
- Operators (`+`, `-`, `==`, etc.)
- Keywords (`if`, `else`, `while`, etc.)
- Trigonometric and mathematical functions (`sqrt`, `log`, `cos`, etc.)
- Punctuation (parentheses, brackets, etc.)

It also handles **invalid characters** by throwing an error instead of crashing.

#### `__init__.py`
Used to easily **import** things from the lexer package. For example, instead of doing:
```python
from lexer.lexer import Lexer
```
You could do:
```python
from lexer import Lexer
```

#### `test_lexer.py`
A well-made lexer should be **testable**. This file uses Python’s `unittest` framework to verify that:

- Tokens are detected properly
- Invalid input is caught
- Keywords and functions are recognized correctly
- Complex expressions like `if sin(30) > 0.5:` are tokenized right

---

### 🧪 Example Usage

Given this input:

```
sin(45) + 3.14 * cos(90) / sqrt(2)
```

You get back a list of tokens like:

```
[FUNCTION(sin), LPAREN(()), INTEGER(45), RPAREN()), PLUS(+), ...]
```

This is how programming languages "see" your code before they understand what it means.

---

### 🔗 Repository

The code lives in a Git repo (link to be submitted later), which is good practice for version control and collaboration.

---

### ✅ Evaluation Notes

You hit all the goals:

- Integers ✅  
- Floats ✅  
- Trig functions ✅  
- Modularity ✅  
- Tests ✅

Which means your lexer is solid and could be extended for more features like strings, comments, or multi-line support.

---

### 🧾 Conclusion

This lab isn’t just about writing Python—it’s about understanding how real programming languages work under the hood. You’ve taken the first step in building a **compiler**, starting with lexical analysis.

Your lexer can now be a base for:

- A calculator  
- A mini programming language  
- A data expression evaluator
