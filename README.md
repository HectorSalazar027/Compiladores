# 🧠 Analizador Léxico y Sintáctico Interactivo

Este proyecto proporciona un **analizador léxico y sintáctico interactivo** con interfaz web. Permite reconocer y clasificar tokens de código Python, así como construir un árbol de sintaxis abstracta (AST). Es accesible desde la línea de comandos o a través de una interfaz web estilizada con TailwindCSS.

---

## 📁 Estructura del Proyecto

```
├── backend
│   ├── Lexer_Analyzer.py           # Analizador léxico (línea de comandos)
│   ├── parser.py                   # Parser con generación de AST
│   ├── server.py                   # API Flask (léxico y sintaxis)
│   ├── IniciarSesion.py            # Módulo adicional (seguridad)
│   ├── GeneradorDeContraseñas.py   # Módulo adicional (seguridad)
│   └── __pycache__/                # Archivos compilados
│
├── frontend
│   ├── css
│   │   └── styles.css              # Estilos personalizados
│   ├── images
│   │   ├── github.png              # Ícono GitHub
│   │   └── Solano.jpg              # Imagen decorativa
│   ├── js
│   │   ├── main.js                 # Lógica de interfaz
│   │   └── particles.min.js        # Efecto de partículas
│   └── index.html                  # Interfaz principal
│
└── README.md                       # Documentación del proyecto
```

---


## 🚀 Cómo Ejecutar

### Opción 1: Consola (solo léxico)

```bash
python server.py
```

Puedes hacer peticiones a la API desde herramientas como Postman o curl:

```bash
curl -X POST http://localhost:5000/analyze -H "Content-Type: application/json" -d '{"code": "def suma(a, b): return a + b", "mode": "lex"}'
```

### Opción 2: Interfaz Web

#### 1. Instala las dependencias

```bash
pip install flask flask-cors
```

#### 2. Ejecuta el backend

```bash
python server.py
```

Esto abrirá la API en `http://localhost:5000`.

#### 3. Abre `index.html` en tu navegador

Solo abre el archivo directamente. La interfaz usará el backend si está corriendo.

---

## 🧪 Funcionalidades

- **Análisis Léxico**:
  - `KEYWORD`, `LITERAL`, `CONSTANT`, `IDENTIFIER`, `OPERATOR`, `PUNCTUATION`
- **Análisis Sintáctico**:
  - Construcción de árbol de sintaxis (AST)
  - Soporte para funciones, asignaciones, condicionales, ciclos y llamadas
- Interfaz moderna con modo claro/oscuro
- Carga de archivos `.py`, `.js`, `.cpp`, `.txt`
- Código de ejemplo precargado
- Copiar y descargar resultados

---

## 👨‍💻 Colaboradores

- [Josue Elizalde](https://github.com/JosJim275)
- [Santiago Medina](https://github.com/sntg-mdn)
- [Héctor Salazar](https://github.com/HectorSalazar027)
- [David Tavera](https://github.com/DavidT328)
- [Jesus Tenorio](https://github.com/JysusAle)
