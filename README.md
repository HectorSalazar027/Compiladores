# 🧠 Analizador Léxico Interactivo

Este proyecto proporciona un **analizador léxico interactivo** con interfaz web, capaz de reconocer y clasificar tokens básicos de código fuente escrito en Python. Puedes usarlo desde línea de comandos o a través de una interfaz web estilizada con TailwindCSS.

---

## 📁 Estructura del Proyecto

```
├── Lexer_Analyzer.py     # Analizador léxico en consola
├── server.py             # Backend con Flask para API REST
├── index.html            # Interfaz web del analizador
├── script.js             # Lógica de frontend y consumo de API
├── /css                  # Estilos personalizados (referenciado)
├── /images               # Imágenes usadas en la UI (como el logo)
```

---

## 🚀 Cómo ejecutar

### Opción 1: Usar desde consola (Python puro)

```bash
python Lexer_Analyzer.py archivo.py
```

Esto mostrará los tokens clasificados por tipo y el total encontrado.

---

### Opción 2: Interfaz Web

#### 1. Instala las dependencias
Se recomienda usar un entorno virtual:

```bash
pip install flask flask-cors
```

#### 2. Ejecuta el servidor

```bash
python server.py
```

Esto abrirá una API REST en `http://localhost:5000`.

#### 3. Abre `index.html` en tu navegador

Solo abre el archivo en tu navegador (no requiere servidor web para el frontend). Asegúrate de que el backend esté corriendo para que la interfaz funcione.

---

## 🛠 Requisitos y Dependencias

### Python
- Python 3.6 o superior
- Bibliotecas:
  - `flask`
  - `flask-cors`

Instalación recomendada:

```bash
pip install -r requirements.txt
```

Contenido sugerido para `requirements.txt`:
```
flask
flask-cors
```

### Navegador
- Cualquier navegador moderno (se recomienda Chrome o Firefox)

---

## 🧪 Funcionalidades

- Clasificación de tokens:
  - `KEYWORD` (`def`, `return`, etc.)
  - `LITERAL` (cadenas de texto)
  - `CONSTANT` (números enteros o flotantes)
  - `IDENTIFIER` (nombres de variables y funciones)
  - `OPERATOR` (`+`, `-`, `==`, etc.)
  - `PUNCTUATION` (`{`, `}`, `(`, `)`, etc.)

- Interfaz intuitiva
- Soporte de tema claro/oscuro
- Carga de archivos `.py`, `.txt`, `.js`, `.cpp`
- Código de ejemplo con un clic

---

## 👨‍💻 Colaboradores

- [Josue Elizalde](https://github.com/JosJim275)
- [Santiago Medina](https://github.com/sntg-mdn)
- [Héctor Salazar](https://github.com/HectorSalazar027)
- [David Tavera](https://github.com/DavidT328)
- [Jesus Tenorio](https://github.com/JysusAle)


