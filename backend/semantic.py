class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.errors = []
        self.current_scope = {}
        self.builtins = {
            "print", "input", "len", "str", "int", "float", "bool", "range",
            "list", "dict", "set", "type", "abs", "max", "min"
        }
        self.class_table = {}
        self.object_table = {}

    def analyze(self, ast):
        for node in ast:
            self.visit(node)
        return self.errors

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        self.errors.append(f"No se puede analizar semánticamente: {type(node).__name__}")

    def visit_FunctionNode(self, node):
        if node.name in self.symbol_table:
            self.errors.append(f"Función '{node.name}' ya está definida.")
        self.symbol_table[node.name] = node
        self.current_scope = {param: "param" for param in node.params}
        for stmt in node.body:
            self.visit(stmt)
        self.current_scope = {}

    def visit_AssignmentNode(self, node):
        self.visit(node.value)
        self.current_scope[node.target] = "var"

    def visit_IdentifierNode(self, node):
        if node.name not in self.current_scope and node.name not in self.symbol_table:
            self.errors.append(f"Variable o función '{node.name}' no está definida.")

    def visit_FunctionCallNode(self, node):
        if node.name not in self.symbol_table and node.name not in self.builtins:
            self.errors.append(f"Llamada a función '{node.name}' no definida.")
        for arg in node.args:
            self.visit(arg)

    def visit_ReturnNode(self, node):
        self.visit(node.value)

    def visit_IfNode(self, node):
        self.visit(node.condition)
        for stmt in node.body:
            self.visit(stmt)
        if node.else_body:
            for stmt in node.else_body:
                self.visit(stmt)

    def visit_WhileNode(self, node):
        self.visit(node.condition)
        for stmt in node.body:
            self.visit(stmt)

    def visit_BinaryOpNode(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_ConstantNode(self, node): pass
    def visit_StringNode(self, node): pass
    def visit_ListNode(self, node):
        for el in node.elements:
            self.visit(el)
    def visit_ImportNode(self, node): pass

    def visit_ClassNode(self, node):
        if node.name in self.class_table:
            self.errors.append(f"Clase '{node.name}' ya está definida.")
        self.class_table[node.name] = node

    def visit_ObjectInstanceNode(self, node):
        if node.class_name not in self.class_table:
            self.errors.append(f"Clase '{node.class_name}' no está definida.")
        self.object_table[node.name] = node.class_name

    def visit_MethodCallNode(self, node):
        if node.object_name not in self.object_table:
            self.errors.append(f"Objeto '{node.object_name}' no está definido.")
            return
        class_name = self.object_table[node.object_name]
        class_node = self.class_table.get(class_name)
        if not class_node:
            self.errors.append(f"Clase '{class_name}' no encontrada.")
            return
        methods = [m.name for m in class_node.body if hasattr(m, "name")]
        if node.method_name not in methods:
            self.errors.append(f"Método '{node.method_name}' no existe en la clase '{class_name}'.")
        for arg in node.args:
            self.visit(arg)
