import re
import sys

# Especificación de los tokens con nombres correctos
TOKEN_SPECIFICATION = [
    ('KEYWORD', r'\b(def|in|import|if|while|return)\b'),
    ('LITERAL', r'f?"[^"]*"'),
    ('CONSTANT', r'\b\d+\.\d+|\b\d+\b'),
    ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z_0-9]*\b'),
    ('OPERATOR', r'==|!=|<=|>=|<|>|=|\+|\-|\*|/'),
    ('PUNCTUATION', r'[\(\):\[\]\{\}]'),
    ('WHITESPACE', r'\s+'),
]

token_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in TOKEN_SPECIFICATION)

def lexer(code):
    tokens = {
        "KEYWORD": [],
        "LITERAL": [],
        "CONSTANT": [],
        "IDENTIFIER": [],
        "OPERATOR": [],
        "PUNCTUATION": []
    }
    total_tokens = 0  
    
    for match in re.finditer(token_regex, code):
        kind = match.lastgroup
        value = match.group(kind)
        if kind != 'WHITESPACE':  
            total_tokens += 1
            if value not in tokens[kind]:
                tokens[kind].append(value)
    
    return tokens, total_tokens

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python Lexer_Analyzer.py archivo.py")
        sys.exit(1)
    
    archivo = sys.argv[1]
    
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            code = f.read()
        
        tokens, total_count = lexer(code)
        
        print("Tokens reconocidos:")
        for category, values in tokens.items():
            print(f"{category} ({len(values)}): {', '.join(values)}")
        
        print(f"\nTotal de tokens: {total_count}")
        
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo}'")
    except Exception as e:
        print(f"Error: {e}")