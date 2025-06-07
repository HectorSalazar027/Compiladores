from flask import Flask, request, jsonify
from flask_cors import CORS
import tokenize
import token as token_module
from io import BytesIO

from parser import Parser
from semantic import SemanticAnalyzer

app = Flask(__name__)
CORS(app)

def to_dict(node):
    if isinstance(node, list):
        return [to_dict(n) for n in node]
    if hasattr(node, "__dict__"):
        return {k: to_dict(v) for k, v in node.__dict__.items()}
    return node

# Mapeo de nombres de token a los nombres deseados
TOKEN_MAP = {
    'NAME': 'identifier',
    'NUMBER': 'constant',
    'STRING': 'literal',
    'NEWLINE': None,
    'NL': None,
    'INDENT': None,
    'DEDENT': None,
    'ENCODING': None,
    'ENDMARKER': None,
    # Operadores/puntuación se procesan en OP
    'OP': 'operator',
}
# Conjunto de puntuación para clasificar OP como punctuation
PUNCTUATION_CHARS = set('()[]{}:.,;')


def lexer(code: str):
    """
    Tokenización con módulo estándar y mapeo de tipos personalizados.
    """
    tokens_list = []
    tokens_dict = {}
    counts = {}
    total_tokens = 0

    reader = BytesIO(code.encode('utf-8')).readline
    for tok in tokenize.tokenize(reader):
        tok_type = tok.type
        tok_name = tokenize.tok_name[tok_type]
        mapped = TOKEN_MAP.get(tok_name)
        # Saltar si no nos interesa este tipo
        if mapped is None:
            continue
        value = tok.string

        # Para OP, distinguir operator vs punctuation
        if tok_name == 'OP':
            mapped = 'punctuation' if value in PUNCTUATION_CHARS else 'operator'

        # Keywords: valores NAME que coinciden con palabras clave de Python
        if mapped == 'identifier' and value in tokenize.kwlist if hasattr(tokenize, 'kwlist') else False:
            mapped = 'keyword'

        # Añadir a estructuras
        tokens_list.append({'type': mapped, 'value': value})
        tokens_dict.setdefault(mapped, [])
        if value not in tokens_dict[mapped]:
            tokens_dict[mapped].append(value)
        counts[mapped] = counts.get(mapped, 0) + 1
        total_tokens += 1

    return {
        'tokens_list': tokens_list,
        'tokens': tokens_dict,
        'counts': counts,
        'total_tokens': total_tokens,
    }

@app.route("/analyze", methods=["POST"])
def analyze():
    req = request.get_json()
    code = req.get("code", "")
    mode = req.get("mode", "lex")

    lex = lexer(code)

    if mode == "lex":
        return jsonify({
            "tokens": lex['tokens'],
            "counts": lex['counts'],
            "total_tokens": lex['total_tokens']
        })

    try:
        parser = Parser(lex['tokens_list'])
        ast = parser.parse()
    except Exception as e:
        print("ERROR EN PARSER:", e)
        return jsonify({"error": str(e)}), 400

    if mode == "sem":
        analyzer = SemanticAnalyzer()
        errors = analyzer.analyze(ast)
        return jsonify({
            "tokens": lex['tokens'],
            "counts": lex['counts'],
            "total_tokens": lex['total_tokens'],
            "ast": to_dict(ast),
            "semantics": errors
        })
    elif mode == "full":
        return jsonify({
            "tokens": lex['tokens'],
            "counts": lex['counts'],
            "total_tokens": lex['total_tokens'],
            "ast": to_dict(ast)
        })

    return jsonify({"error": f"Modo de análisis no reconocido: {mode}"}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)
