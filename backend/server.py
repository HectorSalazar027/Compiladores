from flask import Flask, request, jsonify
from flask_cors import CORS
import tokenize
import token as token_module
import keyword
from io import BytesIO

from parser import Parser
from semantic import SemanticAnalyzer
from assembler import SimpleAssembler
from semantic import link_and_run


app = Flask(__name__)
CORS(app)

def simulate_assembler(code):
    asm = SimpleAssembler()
    return asm.run(code)

def to_dict(node):
    """Convierte cualquier objeto del AST en estructuras JSON-serializables."""
    # 1. Listas
    if isinstance(node, list):
        return [to_dict(n) for n in node]

    # 2. Tuplas   (← NUEVO)
    if isinstance(node, tuple):
        return tuple(to_dict(n) for n in node)

    # 3. Nodos con atributos
    if hasattr(node, "__dict__"):
        return {k: to_dict(v) for k, v in node.__dict__.items()}

    # 4. Primitivos (str, int, bool, None, etc.)
    return node


# === LÉXICO ================================================================

# Mapa de tipos de tokenize → tipos esperados por el Parser (MAYÚSCULA)
TOKEN_MAP = {
    'NAME'      : 'IDENTIFIER',
    'NUMBER'    : 'CONSTANT',
    'STRING'    : 'LITERAL',
    'NEWLINE'   : None,
    'NL'        : None,
    'INDENT'    : None,
    'DEDENT'    : None,
    'ENCODING'  : None,
    # ENDMARKER se ignora en el conteo, pero se añadirá un EOF manual aparte
    'ENDMARKER' : None,
    # El token "OP" se especializa más abajo a OPERATOR o PUNCTUATION
    'OP'        : 'OPERATOR',
}

# Conjunto de caracteres que tratamos como puntuación (no operadores aritméticos)
PUNCTUATION_CHARS = set('()[]{}:.,;')

def lexer(code: str):
    """Devuelve la estructura léxica del código y la lista de tokens para el parser."""
    tokens_list = []
    tokens_dict = {}
    counts = {}
    total_tokens = 0

    reader = BytesIO(code.encode('utf‑8')).readline
    try:
        tok_it = tokenize.tokenize(reader)
        for tok in tok_it:
            tok_name = tokenize.tok_name[tok.type]

            mapped = TOKEN_MAP.get(tok_name, None)
            # Saltar tokens sin relevancia léxica (espacios, indentaciones, etc.)
            if mapped is None:
                continue

            value = tok.string

            # OP → OPERATOR / PUNCTUATION
            if tok_name == 'OP':
                mapped = 'PUNCTUATION' if value in PUNCTUATION_CHARS else 'OPERATOR'

            # Palabras reservadas
            if mapped == 'IDENTIFIER' and value in keyword.kwlist:
                mapped = 'KEYWORD'

            # Agregar token a la lista para el Parser
            tokens_list.append({'type': mapped, 'value': value})

            # Estadísticas para la UI (sin contar EOF, se añadirá después)
            tokens_dict.setdefault(mapped, [])
            if value not in tokens_dict[mapped]:
                tokens_dict[mapped].append(value)
            counts[mapped] = counts.get(mapped, 0) + 1
            total_tokens += 1
    except tokenize.TokenError as err:
        # Caso típico: EOF in multi‑line string / paren, etc.
        # Conservamos lo que llevamos y dejamos que el parser/semántica lo indiquen
        pass

    # Añadir EOF solo para el parser (NO se contabiliza ni se muestra)
    tokens_list.append({'type': 'EOF', 'value': ''})

    return {
        'tokens_list' : tokens_list,
        'tokens'      : tokens_dict,
        'counts'      : counts,
        'total_tokens': total_tokens,
    }

# === API ===================================================================

@app.route('/analyze', methods=['POST'])
def analyze():
    req = request.get_json(force=True)
    code = req.get('code', '')
    mode = req.get('mode', 'lex')  # lex | full | sem
    
    # Ensamblador directo sin lexer/parser
    if mode == 'asm':
        try:
            asm = SimpleAssembler()
            result = asm.run(code)
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    lex = lexer(code)

    # Solo léxico → se devuelve inmediatamente
    if mode == 'lex':
        return jsonify({
            'tokens'      : lex['tokens'],
            'counts'      : lex['counts'],
            'total_tokens': lex['total_tokens']
        })

    # Construcción de AST
    try:
        parser = Parser(lex['tokens_list'])
        ast = parser.parse()
    except Exception as e:
        print('PARSER ERROR:', e)
        return jsonify({'error': str(e)}), 400

    # Con semántica
    if mode == 'sem':
        result = link_and_run(ast)
        if "errors" in result:
            return jsonify({
                'tokens'      : lex['tokens'],
                'counts'      : lex['counts'],
                'total_tokens': lex['total_tokens'],
                'ast'         : to_dict(ast),
                'semantics'   : result["errors"]
            })
        return jsonify({
            'tokens'      : lex['tokens'],
            'counts'      : lex['counts'],
            'total_tokens': lex['total_tokens'],
            'ast'         : to_dict(ast),
            'semantics'   : [],
            'output'      : result["output"]
        })


    # AST sin semántica
    if mode == 'full':
        return jsonify({
            'tokens'      : lex['tokens'],
            'counts'      : lex['counts'],
            'total_tokens': lex['total_tokens'],
            'ast'         : to_dict(ast)
        })

    if mode == 'asm':
        try:
            asm = SimpleAssembler()
            result = asm.run(code)
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)}), 400
        
    return jsonify({'error': f'Modo de análisis no reconocido: {mode}'}), 400

# Entrypoint para uso local
if __name__ == '__main__':
    app.run(debug=True, port=5000)