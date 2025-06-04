# 🧠 Analizador Léxico y Sintáctico Interactivo

Este proyecto proporciona un **analizador léxico y sintáctico interactivo** con interfaz web. Permite reconocer y clasificar tokens de código Python, así como construir un árbol de sintaxis abstracta (AST). Es accesible desde la línea de comandos o a través de una interfaz moderna con soporte de temas claro/oscuro.

---

## 📁 Estructura del Proyecto

```
├── backend
│   ├── Lexer_Analyzer.py           # Analizador léxico (línea de comandos)
│   ├── parser.py                   # Parser con generación de AST
│   ├── server.py                   # API Flask (léxico y sintaxis)
│   ├── IniciarSesion.py            # Módulo adicional (sesión)
│   ├── GeneradorDeContraseñas.py   # Módulo adicional (contraseñas)
│   └── __pycache__/                # Archivos compilados por Python
│
├── frontend
│   ├── css
│   │   └── styles.css              # Estilos personalizados
│   ├── images
│   │   ├── github.png              # Ícono GitHub
│   │   └── Solano.jpg              # Imagen decorativa
│   ├── js
│   │   ├── main.js                 # Lógica de la interfaz
│   │   └── particles.min.js        # Efecto visual de partículas
│   └── index.html                  # Interfaz principal de usuario
│
└── README.md                       # Documentación del proyecto
```

---

## 🚀 Cómo Ejecutar

### Opción 1: Consola (sólo léxico)

```bash
python backend/Lexer_Analyzer.py archivo.py
```

### Opción 2: Interfaz Web (léxico + sintaxis)

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

## ⚙️ ¿Cómo Funciona?

- El usuario ingresa o carga código fuente en Python.
- El backend lo procesa con expresiones regulares para análisis léxico.
- Si se elige modo *Léxico + Sintaxis*, se genera un árbol de sintaxis abstracta (AST).
- El resultado se muestra en la interfaz, junto con botones para copiar, limpiar o descargar.

---

## 🧪 Funcionalidades

- **Análisis Léxico**:
  - Reconocimiento de: `KEYWORD`, `LITERAL`, `CONSTANT`, `IDENTIFIER`, `OPERATOR`, `PUNCTUATION`
- **Análisis Sintáctico**:
  - Construcción del AST con nodos: funciones, ciclos, condiciones, expresiones, llamadas, listas
- **Interfaz Web**:
  - Tema claro/oscuro
  - Soporte para carga de archivos `.py`, `.js`, `.cpp`, `.txt`
  - Ejemplo precargado
  - Exportación de resultados

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

## 🧠 Detalles Técnicos

- El **analizador léxico** usa expresiones regulares para clasificar los tokens.
- El **parser** aplica reglas gramaticales simples para formar el árbol de sintaxis (AST), con clases específicas para nodos como `FunctionNode`, `WhileNode`, `IfNode`, etc.
- El código fuente es transformado en una lista de tokens y luego procesado secuencialmente para construir estructuras anidadas.
- La interfaz está construida con HTML + TailwindCSS, y usa JavaScript moderno (`fetch`, `FileReader`, `Blob`, etc.).

---

## 👨‍💻 Colaboradores

- [Josue Elizalde](https://github.com/JosJim275)
- [Santiago Medina](https://github.com/sntg-mdn)
- [Héctor Salazar](https://github.com/HectorSalazar027)
- [David Tavera](https://github.com/DavidT328)
- [Jesus Tenorio](https://github.com/JysusAle)
