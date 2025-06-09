# Universidad Nacional Autónoma de México  
*Computer Engineering*

## Compilers – Group 5

**Teacher:** M.C. René Adrián Dávila Pérez  
**Delivery date:** June 8, 2025

# Compiler

**Team:** 8

| Account Number | Last Name | Middle Name | First Name(s) |
| -------------- | --------- | ----------- | ------------- |
| 320034489 | Juárez  | Elizalde | Josue |
| 320007354 | Medina  | Guzmán   | Santiago |
| 320064531 | Tavera  | Castillo | David Emmanuel |
| 320781066 | Tenorio | Martínez | Jesús Alejandro |
| 117004023 | Salazar | Rubi     | Héctor Manuel |

**Semester 2025‑2**


---

# 🚀 Compiler Project

## 📖 Introduction

This project implements a complete compiler system, comprising a lexical analyzer, syntax analyzer, semantic analyzer, and a simple assembler, integrated with a user-friendly web interface built using Flask and JavaScript. It provides clear visualization of each compilation phase, including tokenization, AST (Abstract Syntax Tree) construction, semantic validation, and code execution.

## 🎯 Problem Statement

The task is to build a compiler capable of:
- Reading and analyzing source code through multiple compilation stages.
- Supporting fundamental constructs: conditional statements, loops, function definitions, class declarations, and arithmetic/logical operations.
- Simulating execution via an assembler.
- Exposing all functionalities via a web server.

## 🔥 Motivation

We aimed to practically apply theoretical compiler concepts learned in class, exploring language processing stages from lexical analysis to execution. Using Python, Flask, and web technologies allowed us to create an interactive, educational tool demonstrating both high-level and low-level language processing.

## 🎯 Objectives

- **Lexical Analysis:** Identify and classify tokens (keywords, identifiers, literals, operators, punctuation).
- **Syntax Analysis:** Validate grammar structures and build ASTs.
- **Semantic Analysis:** Ensure correct usage of identifiers and constructs.
- **Execution Server:** Interpret and execute code via Flask API.
- **Assembler Simulation:** Execute custom assembly language instructions.

# 🧠 Interactive Lexical, Syntactic & Semantic Analyzer

![Home page](unam.fi.compilers.g5.08/frontend/images/Pagina_principal.png)

An educational **compiler pipeline** that lets you explore every major stage—lexical analysis, parsing, semantic checking, interpretation, and even a *toy* assembler—through a modern web UI backed by a lightweight Flask API.

> **Group 5 · UNAM Computer Engineering · Semester 2025‑2**

---

## 📑 Table of Contents
1. [Project Overview](#project-overview)  
2. [Folder Structure](#folder-structure)  
3. [Prerequisites](#prerequisites)  
4. [Running Locally](#running-locally)  
5. [Supported Analysis Modes](#supported-analysis-modes)  
6. [Theoretical Background](#theoretical-background)  
7. [Compliance with Official PDF Guidelines](#compliance-with-official-pdf-guidelines)  
8. [Extra‑Credit Features](#extra-credit-features)  
9. [Best Practices Adopted](#best-practices-adopted)  
10. [Authors](#authors)

---

## Project Overview
This repository contains:
* **`lexer` & `parser`** that build a full Abstract Syntax Tree (AST) for a Python‑like subset.  
* **`semantic` analysis** that validates scopes, duplicates, and control‑flow misuse.  
* **`interpreter / linker`** that executes the AST when no semantic errors are present.  
* **`SimpleAssembler`** that executes a micro‑assembly language for low‑level insight.  
* **Flask API** exposing all stages (`/analyze` endpoint).  
* **Tailwind‑powered frontend** with light/dark theme, drag‑n‑drop, examples, and particle background.

---

## Folder Structure
```text
unam.fi.compilers.g5.XX/
├── backend
│   ├── assembler.py         # Toy assembler 
│   ├── parser.py            # Recursive‑descent parser → AST
│   ├── semantic.py          # Semantic analyzer & interpreter
│   └── server.py            # Flask API (lex/syntax/semantics/asm)
│
├── frontend
│   ├── css/styles.css       # Tailwind overrides
│   ├── js/main.js           # UI logic & API calls
│   ├── images/              # Assets
│   └── index.html           # Main interface
│
└── README.md                
```

---

## Prerequisites
### Python ≥ 3.8
```bash
pip install flask flask-cors
# optional: python -m venv venv
```

### Browser
Any modern browser (Chrome / Firefox / Edge).

---

## Running Locally
1. **Install dependencies**
   ```bash
   pip install flask flask-cors
   ```
2. **Start the backend**
   ```bash
   python backend/server.py
   ```
3. **Open the frontend**  
   Double‑click `frontend/index.html` or serve it with your favourite static server.

![How to run the server.py file](unam.fi.compilers.g5.08/frontend/images/Ejecución.png)   

---

## Supported Analysis Modes
| Mode | What you get | Endpoint payload (`mode`) |
|------|--------------|---------------------------|
| **Lexical** | Token categories, counts, and unique values. | `lex` |
| **Lexical + Syntax** | Full AST in JSON. | `full` |
| **Lexical + Syntax + Semantic** | AST • semantic‑error list • program output. | `sem` |
| **Assembler** | Simulated registers & output for custom mnemonics. | `asm` |

---


### 1. Compilation Phases
 
* **Preloaded examples**
![Preloaded examples](unam.fi.compilers.g5.08/frontend/images/Ejemplopre.png)   

* **Lexical Analysis** – converts raw text into *tokens* using Python’s `tokenize`, mapping them to categories (`KEYWORD`, `IDENTIFIER`, …).

![Lexical Analysis](unam.fi.compilers.g5.08/frontend/images/AnalisisLexico.png)  

* **Parsing** – builds an **AST** via a hand‑written recursive‑descent parser that recognises functions, classes, control flow, data literals, and augmented assignments.

![Parsing](unam.fi.compilers.g5.08/frontend/images/parser.png)
![Syntax Tree (AST)](unam.fi.compilers.g5.08/frontend/images/parser1.png)

* **Semantic Analysis** – traverses the AST (visitor pattern) to ensure declarations, scope, and control‑flow rules are respected.


![Semantic Analysis](unam.fi.compilers.g5.08/frontend/images/semantic.png)

![Program exit](unam.fi.compilers.g5.08/frontend/images/semantic1.png)


* **Interpretation / Linkage** – executes the AST when semantics are valid, recording side‑effects and producing runtime **output**.
* **Assembly Execution (Bonus)** – a *SimpleAssembler* interprets an 8/16‑bit register set with arithmetic, logic, jumps, and I/O.

### 2. Execution Architecture
```
   Browser  ⇆  Flask API  ⇆  Core compiler modules  ⇆  (optional) Assembler VM
```
*Front‑end* sends code & mode → **Flask** delegates to lex/parse/sem/asm → returns JSON → UI renders tokens, AST trees, errors, or terminal‑like output.

---


## 📚 Theoretical Framework

The compiler is structured in four main phases:

### Lexical Analyzer
- Uses Python's `tokenize` module and custom mappings for token identification.
- Classifies tokens into categories like `KEYWORD`, `IDENTIFIER`, `CONSTANT`, `LITERAL`, `OPERATOR`, and `PUNCTUATION`.

### Syntax Analyzer
- Implements a recursive descent parser.
- Generates an Abstract Syntax Tree (AST) representing program structure.
- Supports functions, classes, control structures (`if`, `while`, `for`), and compound statements (`try-except`).

### Semantic Analyzer
- Traverses the AST to ensure correctness of declarations and scope.
- Detects semantic errors such as undeclared variables, misuse of `return`, and invalid operations.

### Simple Assembler
- Simulates basic assembly instructions (`MOV`, `ADD`, `CMP`, `JMP`, `PRINT`, `HALT`).
- Manages registers, arithmetic/logical operations, conditional jumps, and program termination.

## 💻 Web Interface

- Developed using HTML, CSS, and JavaScript.
- Allows users to choose analysis modes (Lexical, Syntax, Semantic, Assembler).
- Dynamically visualizes tokens, ASTs, semantic errors, and execution outputs.

---


## Compliance with Official PDF Guidelines
| Requirement (simplified) | Implemented? | Evidence |
|--------------------------|--------------|----------|
| Lexical analyzer | ✅ | `server.lexer`, `tokenize` mapping |
| Parser generating AST | ✅ | `parser.py` classes & `Parser.parse()` |
| Semantic analyzer | ✅ | `semantic.py::SemanticAnalyzer` |
| Interpreter / Linker | ✅ | `semantic.py::Interpreter` & `link_and_run` |
| Simplified Assembler | ✅ | `assembler.py::SimpleAssembler` |
| Web server API | ✅ | `server.py` Flask routes |
| GUI / Frontend | ✅ | `frontend/index.html`, `main.js` |
| Documentation in PDF format | ✅ | `Compilers_Documentation.pdf` |
| Results & Use‑case section | ✅ | *Chapter 4* of the PDF |
| Conclusions & References | ✅ | *Ch. 5‑6* of the PDF |

---

## Extra‑Credit Features
| Extra point | Status | Brief note |
|-------------|--------|------------|
| **Data Structures** | ✅ | Custom `ASTNode` hierarchy, symbol tables (`dict`), register file (`dict`). |
| **Error Handler** | ✅ | Lexer skips invalid tokens; SemanticAnalyzer accrues detailed error strings; UI maps technical errors to friendly Spanish. |
| **Object‑Oriented Programming (TDA)** | ✅ | Core compiler built around classes (`Lexer`, `Parser`, `NodeVisitor`, etc.); frontend uses modular JS. |

- **Extras to consider**

- Change of Theme (Dark or Light)
![Change of Theme (Dark or Light)](unam.fi.compilers.g5.08/frontend/images/Tema.png)

- Based on the Z80 Assembler architecture
![Based on the Z80 Assembler architecture](unam.fi.compilers.g5.08/frontend/images/EjemplosA.png)
![Assembler code](unam.fi.compilers.g5.08/frontend/images/Programa1.png)
![Program analysis and output:](unam.fi.compilers.g5.08/frontend/images/Programa2.png)

- Handling syntactical errors
![Syntax error in "print"](unam.fi.compilers.g5.08/frontend/images/ManejoError.png)

## 🚨 Semantic Error Example

```python
return 5
```

**Produces error**: `'return' fuera de una función.`

---

- Conditionals
![if-else](unam.fi.compilers.g5.08/frontend/images/Condicional.png)
![Program Output](unam.fi.compilers.g5.08/frontend/images/Condicional1.png)

---

## Best Practices Adopted
* **Layered architecture** separates UI, API, and core logic.
* **PEP‑8** compliant code, descriptive names, docstrings.
* Defensive programming with explicit **validation** in assembler & parser.
* Browser‑side **theme toggle** and small visual feedback helpers.
* Placeholder tests (see `tests/` soon) and ESLint/Tailwind config.

---


## 📌 Conclusions

Building this compiler reinforced our understanding of **lexical**, **syntactic**, and **semantic analysis**.  
Python's capabilities simplified **string processing**, while **Flask** allowed seamless frontend integration.  
The **assembler** further enriched our understanding by simulating **low-level execution**.

---

## 📚 References

## 📚 References

1. TREMBLAY, Jean-Paul, and SORENSON, Paul. *The Theory and Practice of Compiler Writing*. McGraw-Hill, 1985.  
2. AHO, Alfred, SETHI, Ravi, and ULLMAN, Jeffrey D. *Compiladores: Principios, técnicas y herramientas*. Addison-Wesley Iberoamericana, 2000.  
3. AHO, Alfred V., LAM, Monica S., SETHI, Ravi, and ULLMAN, Jeffrey D. *Compilers: Principles, Techniques, and Tools*. 2nd ed., Pearson Education, 2007.  
4. WAITE, W. M., and GOOS, G. *Compiler Construction*. Springer Science & Business Media, 2012.  
5. WIRTH, Niklaus. *Compiler Construction*. Vol. 1, Addison-Wesley, 1996.  
6. LOUDEN, Kenneth C. *Compiler Construction: Principles and Practice*. PWS Publishing Co., 1997.  
7. STEELE, Peter W., and TOMEK, Ivan. *Z80 Assembly Language Programming*. Computer Science Press, Inc., 1987.  
8. ["Abstract Syntax Tree (AST) in Java"](https://www.geeksforgeeks.org/abstract-syntax-tree-ast-in-java/), GeeksforGeeks, Aug. 12, 2021.  
9. ["Semantic Analysis in Compiler Design"](https://www.geeksforgeeks.org/semantic-analysis-in-compiler-design/), GeeksforGeeks, Apr. 22, 2020.  
10. ["Documentation – Arm Developer"](https://developer.arm.com/documentation), Arm Developer.  
11. ["Kotlin Programming Language"](https://kotlinlang.org/), Kotlin.  
12. ConsoleTVs, ["VirtualMachine/src/vm.cpp at master · ConsoleTVs/VirtualMachine"](https://github.com/ConsoleTVs/VirtualMachine/blob/master/src/vm.cpp), GitHub.  
13. ["Phases of a Compiler"](https://www.geeksforgeeks.org/phases-of-a-compiler/), GeeksforGeeks, Jan. 25, 2025.  


---

## Authors
* Héctor Salazar  
* Jesús Tenorio  
* Josué Elizalde  
* Santiago Medina  
* David Tavera  

*For academic purposes only.*  
