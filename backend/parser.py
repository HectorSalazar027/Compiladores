# Representa un token con tipo y valor, usado por el parser
class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

# Clase base para nodos del árbol de sintaxis abstracta (AST)
class ASTNode:
    pass

# Nodo para representar una función
class FunctionNode(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

# Nodo para representar un ciclo while
class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

# Nodo para representar una instrucción return
class ReturnNode(ASTNode):
    def __init__(self, value):
        self.value = value

# Nodo de asignación: variable = valor
class AssignmentNode(ASTNode):
    def __init__(self, target, value):
        self.target = target
        self.value = value

# Nodo para operaciones binarias: a + b, x * y, etc.
class BinaryOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

# Nodo para representar un identificador (nombre de variable)
class IdentifierNode(ASTNode):
    def __init__(self, name):
        self.name = name

# Nodo para representar constantes numéricas
class ConstantNode(ASTNode):
    def __init__(self, value):
        self.value = value

# Nodo para llamada a función: f(x, y)
class FunctionCallNode(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

# Nodo para condicional if (con else opcional)
class IfNode(ASTNode):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

# Nodo para representar cadenas de texto
class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value

# Nodo para listas: [1, 2, 3]
class ListNode(ASTNode):
    def __init__(self, elements):
        self.elements = elements

# Nodo para declaraciones de import
class ImportNode(ASTNode):
    def __init__(self, module):
        self.module = module

# Nodo para representar una clase
class ClassNode(ASTNode):
    def __init__(self, name, body):
        self.name = name
        self.body = body

# Nodo para representar un método dentro de una clase
class MethodNode(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

# Nodo para representar la creación de un objeto
class ObjectInstanceNode(ASTNode):
    def __init__(self, name, class_name):
        self.name = name
        self.class_name = class_name

# Nodo para representar una llamada a método de un objeto
class MethodCallNode(ASTNode):
    def __init__(self, object_name, method_name, args):
        self.object_name = object_name
        self.method_name = method_name
        self.args = args

# Clase principal que convierte tokens en un AST
class Parser:
    def __init__(self, token_list):
        self.tokens = [Token(tok["type"], tok["value"]) for tok in token_list]  # Lista de tokens
        self.pos = 0  # Posición actual en la lista de tokens

    # Devuelve el token actual
    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token("EOF", "")

    # Mira tokens siguientes sin consumirlos
    def lookahead(self, n =1):
        if self.pos + n < len(self.tokens):
            return self.tokens[self.pos + n]
        return Token("EOF", "")

    # Consume un token si es del tipo esperado
    def consume(self, expected_type=None):
        token = self.current_token()
        if expected_type and token.type != expected_type:
            raise SyntaxError(f"Expected {expected_type} but got {token.type}")
        self.pos += 1
        return token

    # Punto de entrada: analiza todos los tokens y devuelve el AST
    def parse(self):
        ast = []
        while self.current_token().type != "EOF":
            if self.current_token().value == "def":
                ast.append(self.parse_function())
            elif self.current_token().value == "class":
                ast.append(self.parse_class())
            elif self.current_token().value == "while":
                ast.append(self.parse_while())
            elif self.current_token().value == "if":
                ast.append(self.parse_if())
            elif self.current_token().value == "import":
                ast.append(self.parse_import())
            else:
                ast.append(self.parse_statement())
        return ast

    # Parseo de función: def nombre(parametros):
    def parse_function(self):
        self.consume("KEYWORD")  # def
        name = self.consume("IDENTIFIER").value
        self.consume("PUNCTUATION")  # (
        params = []
        while self.current_token().value != ")":
            params.append(self.consume("IDENTIFIER").value)
            if self.current_token().value == ",":
                self.consume("PUNCTUATION")
        self.consume("PUNCTUATION")  # )
        self.consume("PUNCTUATION")  # :
        body = self.parse_block()
        return FunctionNode(name, params, body)

    # Parseo de clase: class Nombre:
    def parse_class(self):
        self.consume("KEYWORD")
        name = self.consume("IDENTIFIER").value
        self.consume("PUNCTUATION")  # :
        body = self.parse_block()
        return ClassNode(name, body)

    # Parseo de bucle while
    def parse_while(self):
        self.consume("KEYWORD")  # while
        condition = self.parse_expression()
        self.consume("PUNCTUATION")  # :
        body = self.parse_block()
        return WhileNode(condition, body)

    # Parseo de if (con else opcional)
    def parse_if(self):
        self.consume("KEYWORD")  # if
        condition = self.parse_expression()
        self.consume("PUNCTUATION")  # :
        body = self.parse_block()
        else_body = None
        if self.current_token().value == "else":
            self.consume("KEYWORD")
            self.consume("PUNCTUATION")  # :
            else_body = self.parse_block()
        return IfNode(condition, body, else_body)

    # Parseo de import
    def parse_import(self):
        self.consume("KEYWORD")  # import
        module = self.consume("IDENTIFIER").value
        return ImportNode(module)

    # Parseo de un bloque (conjunto de sentencias)
    def parse_block(self):
        statements = []
        while self.pos < len(self.tokens):
            token = self.current_token()
            if token.value in ("def", "class", "while", "if", "import", "else"):
                break
            try:
                statements.append(self.parse_statement())
            except SyntaxError:
                break
        return statements

    # Parseo de una sola sentencia
    def parse_statement(self):
        token = self.current_token()
        if token.type == "IDENTIFIER":
            if self.lookahead().value == "(":  # Llamada a función
                return self.parse_expression()
            elif self.lookahead().value == "=" and self.lookahead(2).type == "IDENTIFIER":  # Instancia de clase
                target = self.consume("IDENTIFIER").value
                self.consume("OPERATOR")
                class_name = self.consume("IDENTIFIER").value
                self.consume("PUNCTUATION")
                return ObjectInstanceNode(target, class_name)
            elif self.lookahead().value == ".":  # Llamada a método
                obj = self.consume("IDENTIFIER").value
                self.consume("PUNCTUATION")
                method = self.consume("IDENTIFIER").value
                self.consume("PUNCTUATION")  # (
                args = []
                while self.current_token().value != ")":
                    args.append(self.parse_expression())
                    if self.current_token().value == ",":
                        self.consume("PUNCTUATION")
                self.consume("PUNCTUATION")  # )
                return MethodCallNode(obj, method, args)
            else:  # Asignación simple
                target = self.consume("IDENTIFIER").value
                self.consume("OPERATOR")
                value = self.parse_expression()
                return AssignmentNode(target, value)
        elif token.value == "return":
            self.consume("KEYWORD")
            value = self.parse_expression()
            return ReturnNode(value)
        else:
            raise SyntaxError(f"Unknown statement starting with {token}")

    # Parseo de una expresión (operadores binarios)
    def parse_expression(self):
        left = self.parse_term()
        while self.current_token().type == "OPERATOR" and self.current_token().value in ("+", "-", "<", ">", "==", "*"):
            op = self.consume("OPERATOR").value
            right = self.parse_term()
            left = BinaryOpNode(left, op, right)
        return left

    # Parseo de términos simples: constantes, variables, cadenas, listas, llamadas
    def parse_term(self):
        token = self.current_token()
        if token.type == "CONSTANT":
            return ConstantNode(self.consume("CONSTANT").value)
        elif token.type == "LITERAL":
            return StringNode(self.consume("LITERAL").value)
        elif token.type == "IDENTIFIER":
            name = self.consume("IDENTIFIER").value
            if self.current_token().value == "(":  # llamada a función
                self.consume("PUNCTUATION")  # (
                args = []
                while self.current_token().value != ")":
                    args.append(self.parse_expression())
                    if self.current_token().value == ",":
                        self.consume("PUNCTUATION")
                self.consume("PUNCTUATION")  # )
                return FunctionCallNode(name, args)
            return IdentifierNode(name)
        elif token.value == "[":  # lista
            self.consume("PUNCTUATION")
            elements = []
            while self.current_token().value != "]":
                elements.append(self.parse_expression())
                if self.current_token().value == ",":
                    self.consume("PUNCTUATION")
            self.consume("PUNCTUATION")  # ]
            return ListNode(elements)
        elif token.value == "(":  # expresión entre paréntesis
            self.consume("PUNCTUATION")
            expr = self.parse_expression()
            self.consume("PUNCTUATION")
            return expr
        else:
            raise SyntaxError(f"Unexpected token {token}")
