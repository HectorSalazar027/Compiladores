# 🧠 Analizador Léxico, Sintáctico y Semántico Interactivo

Este proyecto implementa un **analizador léxico, sintáctico y semántico interactivo**, complementado con un **linker/interpreter** y soporte opcional para modo ensamblador. Está diseñado siguiendo principios de arquitectura modular, con una interfaz web moderna y clara, y un backend basado en Flask.

El sistema permite validar, interpretar y ejecutar fragmentos de código fuente en un subconjunto de Python, y también ejecutar instrucciones de ensamblador personalizadas.

---

## 📁 Estructura del Proyecto

```
unam.fi.compilers.g5.XX/
├── backend
│   ├── assembler.py                # Modo ensamblador personalizado
│   ├── parser.py                   # Parser con generación de AST
│   ├── server.py                   # API Flask (léxico y sintaxis)
│   └── __pycache__/                # Archivos compilados por Python
│
├── frontend
│   ├── css
│   │   └── styles.css              # Estilos personalizados
│   ├── images
│   │   ├── github.png              # Ícono GitHub
│   ├── js
│   │   ├── main.js                 # Lógica de la interfaz
│   │   └── particles.min.js        # Efecto visual de partículas
│   └── index.html                  # Interfaz principal de usuario
│
└── README.md                       # Documentación del proyecto
```

---
## 🛠 Requisitos

### Python
- Python 3.6 o superior
- Instalar con:

```bash
pip install flask flask-cors
```

> También puedes crear un entorno virtual con `python -m venv venv`

### Navegador
- Cualquier navegador moderno (Chrome, Firefox, Edge)

---

## 🚀 Cómo Ejecutar

1. **Instalar dependencias**:

```bash
pip install flask flask-cors
```

2. **Ejecutar servidor backend**:

```bash
python backend/server.py
```

3. **Abrir la interfaz**:

Abre `frontend/index.html` en tu navegador.


---

## 💡 Modos de Análisis Soportados

### ✅ Léxico
- Clasificación de tokens: `KEYWORD`, `IDENTIFIER`, `CONSTANT`, `LITERAL`, `OPERATOR`, `PUNCTUATION`

### ✅ Léxico + Sintaxis
- Generación de AST con nodos: `FunctionNode`, `WhileNode`, `IfNode`, `ForNode`, `TryNode`, etc.
- **Análisis Sintáctico**:
  - Construcción del AST con nodos: funciones, ciclos, condiciones, expresiones, llamadas de funciones, listas
- **Soporte de estructuras de control extendidas:**
  - Definiciones: import (con alias), def, class
  - Sentencias de control: if/elif/else, while, for‑in, try/except, pass, return
  - Estructuras de datos: lista, tupla, diccionario
  - Operadores compuestos: +=, -=, *=, /=, etc.
  - Programación orientada a objetos: instanciación y llamada a métodos simples
  - Uso de in tanto en bucles como en expresiones condicionales

### ✅ Léxico + Sintaxis + Semántico (con ejecución)
- **Análisis semántico completo**:
  - Detección de errores: variables no declaradas, `break`/`return` mal ubicados, clases duplicadas, etc.
- **Linker**: ejecuta el AST si no hay errores semánticos.
  - Simula la ejecución del código con una salida `output` como resultado.

### ✅ Ensamblador (extra)
- Instrucciones personalizadas como: `MOV`, `ADD`, `CMP`, `JMP`, `PRINT`, `HALT`
- Ejecución directa sin parser ni AST.
- Uso de registros simulados.

---

## 🧠 Ejemplo de Uso

```python
def suma(a, b):
    return a + b

print(suma(5, 10))
```

> En modo *Léxico + Sintaxis + Semántico*, se mostrará el AST, se validará semánticamente y se mostrará el resultado de la ejecución: `15`.

---

## ✨ Funcionalidades Adicionales 

- **Interfaz Web**
  - 🌗 **Tema claro/oscuro**
  - 📂 **Carga de archivos** `.py`, `.js`, `.cpp`, `.txt`
  - 🧠 **Interfaz intuitiva** con visualización progresiva de tokens, AST y errores
- 🧪 **Validaciones semánticas avanzadas**
- 📦 **Arquitectura modular con orientación a objetos**
- ⚠️ **Manejo de errores semánticos con mensajes claros**

---

## 📦 Buenas Prácticas

- Código dividido por capas: `parser`, `semantic`, `assembler`, `server`
- Uso de **clases y TDAs** (`NodeVisitor`, `Interpreter`, `SemanticAnalyzer`)
- Interfaz desacoplada del backend (consume API vía `fetch`)
- Incluye ejemplos automáticos y mensajes de ayuda

---

## 📜 Requisitos Técnicos

- **Python** 3.6+
- **Flask** + **flask-cors**
- Navegador moderno (Chrome, Firefox, etc.)

---

## 👨‍💻 Autores

- [Héctor Salazar](https://github.com/HectorSalazar027)
- [Jesus Tenorio](https://github.com/JysusAle)

---

