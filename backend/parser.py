
class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


class ASTNode:
    pass

class FunctionNode(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ReturnNode(ASTNode):
    def __init__(self, value):
        self.value = value

class AssignmentNode(ASTNode):
    def __init__(self, target, value):
        self.target = target
        self.value = value

class BinaryOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class IdentifierNode(ASTNode):
    def __init__(self, name):
        self.name = name

class ConstantNode(ASTNode):
    def __init__(self, value):
        self.value = value

class FunctionCallNode(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class IfNode(ASTNode):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value

class ListNode(ASTNode):
    def __init__(self, elements):
        self.elements = elements

class ImportNode(ASTNode):
    def __init__(self, module):
        self.module = module


class Parser:
    def __init__(self, token_list):
        self.tokens = [Token(tok["type"], tok["value"]) for tok in token_list]
        self.pos = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token("EOF", "")

    def lookahead(self):
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return Token("EOF", "")

    def consume(self, expected_type=None):
        token = self.current_token()
        if expected_type and token.type != expected_type:
            raise SyntaxError(f"Expected {expected_type} but got {token.type}")
        self.pos += 1
        return token

    def parse(self):
        ast = []
        while self.current_token().type != "EOF":
            if self.current_token().value == "def":
                ast.append(self.parse_function())
            elif self.current_token().value == "while":
                ast.append(self.parse_while())
            elif self.current_token().value == "if":
                ast.append(self.parse_if())
            elif self.current_token().value == "import":
                ast.append(self.parse_import())
            else:
                ast.append(self.parse_statement())
        return ast

    def parse_function(self):
        self.consume("KEYWORD")  # def
        name = self.consume("IDENTIFIER").value
        self.consume("PUNCTUATION")  # (
        params = []
        while True:
            if self.current_token().type == "PUNCTUATION" and self.current_token().value == ")":
                break
            if self.current_token().type != "IDENTIFIER":
                raise SyntaxError(f"Expected IDENTIFIER in parameter list but got {self.current_token().type}")
            param = self.consume("IDENTIFIER").value
            params.append(param)
            if self.current_token().value == ",":
                self.consume("PUNCTUATION")
            elif self.current_token().value == ")":
                break
            else:
                raise SyntaxError(f"Unexpected token in parameter list: {self.current_token()}")
        self.consume("PUNCTUATION")  # )
        self.consume("PUNCTUATION")  # :
        body = self.parse_block()
        return FunctionNode(name, params, body)

    def parse_while(self):
        self.consume("KEYWORD")  # while
        condition = self.parse_expression()
        self.consume("PUNCTUATION")  # :
        body = self.parse_block()
        return WhileNode(condition, body)

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

    def parse_import(self):
        self.consume("KEYWORD")  # import
        module = self.consume("IDENTIFIER").value
        return ImportNode(module)

    def parse_block(self):
        statements = []
        while self.pos < len(self.tokens):
            token = self.current_token()
            if token.value in ("def", "while", "if", "import", "else"):
                break
            try:
                statements.append(self.parse_statement())
            except SyntaxError:
                break
        return statements

    def parse_statement(self):
        token = self.current_token()
        if token.type == "IDENTIFIER":
            if self.lookahead().value == "(":
                return self.parse_expression()
            target = self.consume("IDENTIFIER").value
            self.consume("OPERATOR")  # =
            value = self.parse_expression()
            return AssignmentNode(target, value)
        elif token.value == "return":
            self.consume("KEYWORD")
            value = self.parse_expression()
            return ReturnNode(value)
        else:
            raise SyntaxError(f"Unknown statement starting with {token}")

    def parse_expression(self):
        left = self.parse_term()
        while self.current_token().type == "OPERATOR" and self.current_token().value in ("+", "-", "<", ">", "==", "*"):
            op = self.consume("OPERATOR").value
            right = self.parse_term()
            left = BinaryOpNode(left, op, right)
        return left

    def parse_term(self):
        token = self.current_token()
        if token.type == "CONSTANT":
            return ConstantNode(self.consume("CONSTANT").value)
        elif token.type == "LITERAL":
            return StringNode(self.consume("LITERAL").value)
        elif token.type == "IDENTIFIER":
            name = self.consume("IDENTIFIER").value
            if self.current_token().value == "(":
                self.consume("PUNCTUATION")  # (
                args = []
                while self.current_token().value != ")":
                    args.append(self.parse_expression())
                    if self.current_token().value == ",":
                        self.consume("PUNCTUATION")
                self.consume("PUNCTUATION")  # )
                return FunctionCallNode(name, args)
            return IdentifierNode(name)
        elif token.value == "[":
            self.consume("PUNCTUATION")
            elements = []
            while self.current_token().value != "]":
                elements.append(self.parse_expression())
                if self.current_token().value == ",":
                    self.consume("PUNCTUATION")
            self.consume("PUNCTUATION")  # ]
            return ListNode(elements)
        elif token.value == "(":
            self.consume("PUNCTUATION")
            expr = self.parse_expression()
            self.consume("PUNCTUATION")
            return expr
        else:
            raise SyntaxError(f"Unexpected token {token}")
