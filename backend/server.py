from flask import Flask, request, jsonify
from flask_cors import CORS
import re
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

TOKEN_SPECIFICATION = [
    ('KEYWORD', r'\b(class|def|return|if|else|while|True|False|import|for|in|range|print|input)\b'),
    ('LITERAL', r'f?"[^"\n]*"'),  
    ('CONSTANT',    r'\b\d+\.\d+|\b\d+\b'),
    ('IDENTIFIER',  r'\b[a-zA-Z_][a-zA-Z_0-9]*\b'),
    ('OPERATOR',    r'==|!=|<=|>=|<|>|=|\+|\-|\*|/'),
    ('PUNCTUATION', r'[\(\):,\[\]\{\}]'),
    ('WHITESPACE',  r'\s+'),
]
token_regex = '|'.join(f'(?P<{n}>{p})' for n, p in TOKEN_SPECIFICATION)

def lexer(code: str):
    tokens_list = []
    tokens_dict = {k: [] for k, _ in TOKEN_SPECIFICATION if k != "WHITESPACE"}
    counts = {k: 0 for k in tokens_dict}
    total_tokens = 0

    for m in re.finditer(token_regex, code):
        kind = m.lastgroup
        value = m.group(kind)
        if kind == "WHITESPACE":
            continue
        tokens_list.append({"type": kind, "value": value})
        if value not in tokens_dict[kind]:
            tokens_dict[kind].append(value)
        counts[kind] += 1
        total_tokens += 1

    return {
        "tokens_list": tokens_list,
        "tokens": tokens_dict,
        "counts": counts,
        "total_tokens": total_tokens,
    }
@app.route("/analyze", methods=["POST"])
def analyze():
    req = request.get_json()
    code = req.get("code", "")
    mode = req.get("mode", "lex")

    lex = lexer(code)

    # Si es sólo análisis léxico, devolver directamente
    if mode == "lex":
        return jsonify({
            "tokens": lex["tokens"],
            "counts": lex["counts"],
            "total_tokens": lex["total_tokens"]
        })

    # Si requiere análisis sintáctico o semántico
    try:
        parser = Parser(lex["tokens_list"])
        ast = parser.parse()
    except Exception as e:
        print("ERROR EN PARSER:", e)
        return jsonify({"error": str(e)}), 400

    if mode == "sem":
        analyzer = SemanticAnalyzer()
        errors = analyzer.analyze(ast)

        return jsonify({
            "tokens": lex["tokens"],
            "counts": lex["counts"],
            "total_tokens": lex["total_tokens"],
            "ast": to_dict(ast),
            "semantics": errors
        })

    elif mode == "full":
        return jsonify({
            "tokens": lex["tokens"],
            "counts": lex["counts"],
            "total_tokens": lex["total_tokens"],
            "ast": to_dict(ast)
        })

    return jsonify({"error": f"Modo de análisis no reconocido: {mode}"}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)
