# Universidad Nacional Autónoma de México  
*Computer Engineering*

## Compilers – Group 5

**Teacher:** M.C. René Adrián Dávila Pérez  
**Delivery date:** June 8, 2025

# Compiler

**Team:** 8

| Account Number | Last Name | Middle Name | First Name(s) |
| -------------- | --------- | ----------- | ------------- |
| 320034489 | Juárez  | Elizalde | José |
| 320007354 | Medina  | Guzmán   | Santiago |
| 320064531 | Tavera  | Castillo | David Emmanuel |
| 320781066 | Tenorio | Martínez | Jesús Alejandro |
| 117004023 | Salazar | Rubi     | Héctor Manuel |

**Semester 2025‑2**


---


# 🧠 Interactive Lexical, Syntactic & Semantic Analyzer

![Home page](unam.fi.compilers.g5.08\frontend\images\Pagina_principal.png)

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
│   ├── assembler.py         # Toy assembler & VM
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
└── README.md                # 🇲🇽 Spanish reference (legacy)
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

![How to run the server.py file](frontend/images/Ejecución.png)   

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
![Preloaded examples](frontend/images/Ejemplos_Precargados.png)   

* **Lexical Analysis** – converts raw text into *tokens* using Python’s `tokenize`, mapping them to categories (`KEYWORD`, `IDENTIFIER`, …).
   ![Lexical Analysis](frontend/images/AnalisisLexico.png)  

* **Parsing** – builds an **AST** via a hand‑written recursive‑descent parser that recognises functions, classes, control flow, data literals, and augmented assignments.
   ![Parsing](frontend/images/parser.png)
   ![Syntax Tree (AST)](frontend/images/parser1.png)
* **Semantic Analysis** – traverses the AST (visitor pattern) to ensure declarations, scope, and control‑flow rules are respected.
   ![Semantic Analysis](frontend/images/semantic.png)
   ![Program exit](frontend/images/semantic1.png)
* **Interpretation / Linkage** – executes the AST when semantics are valid, recording side‑effects and producing runtime **output**.
* **Assembly Execution (Bonus)** – a *SimpleAssembler* interprets an 8/16‑bit register set with arithmetic, logic, jumps, and I/O.

### 2. Execution Architecture
```
   Browser  ⇆  Flask API  ⇆  Core compiler modules  ⇆  (optional) Assembler VM
```
*Front‑end* sends code & mode → **Flask** delegates to lex/parse/sem/asm → returns JSON → UI renders tokens, AST trees, errors, or terminal‑like output.

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
![Change of Theme (Dark or Light)](frontend/images/Tema.png)

- Based on the Z80 Assembler architecture
![Based on the Z80 Assembler architecture](frontend/images/EjemplosA.png)
![Assembler code](frontend/images/Programa1.png)
![Program analysis and output:](frontend/images/Programa2.png)

- Handling syntactical errors
![Syntax error in "print"](frontend/images/ManejoError.png)

- Conditionals
![if-else](frontend/images/Condicional.png)
![Program Output](frontend/images/Condicional1.png)

---

## Best Practices Adopted
* **Layered architecture** separates UI, API, and core logic.
* **PEP‑8** compliant code, descriptive names, docstrings.
* Defensive programming with explicit **validation** in assembler & parser.
* Browser‑side **theme toggle** and small visual feedback helpers.
* Placeholder tests (see `tests/` soon) and ESLint/Tailwind config.

---

## Authors
* Héctor Salazar  
* Jesús Tenorio  
* Josué Elizalde  
* Santiago Medina  
* David Tavera  

*For academic purposes only.*  
