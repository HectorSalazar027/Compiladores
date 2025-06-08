
from __future__ import annotations

import operator as _op
import builtins as _py_builtins
from typing import Any, Dict, List, Set, Tuple

# ---------------------------------------------------------------------
#  Importación de nodos del AST
# ---------------------------------------------------------------------
from parser import (  # type: ignore
    ASTNode,
    ProgramNode,
    FunctionNode,
    ClassNode,
    ImportNode,
    WhileNode,
    ForNode,
    IfNode,
    TryNode,
    ExceptHandlerNode,
    ReturnNode,
    BreakNode,
    PassNode,
    AssignmentNode,
    AugmentedAssignmentNode,
    IdentifierNode,
    ConstantNode,
    StringNode,
    ListNode,
    DictNode,
    TupleNode,
    UnaryOpNode,
    BinaryOpNode,
    FunctionCallNode,
    MethodCallNode,
)

# ---------------------------------------------------------------------
#  Infraestructura de visitante genérico
# ---------------------------------------------------------------------
class NodeVisitor:
    """Visitor genérico con *double dispatch* minimalista."""

    def visit(self, node: ASTNode):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node: ASTNode):
        for attr in vars(node).values():
            if isinstance(attr, list):
                for item in attr:
                    if isinstance(item, ASTNode):
                        self.visit(item)
            elif isinstance(attr, ASTNode):
                self.visit(attr)

# ---------------------------------------------------------------------
#  1) Analizador semántico
# ---------------------------------------------------------------------
class SemanticAnalyzer(NodeVisitor):
    """Valida símbolos, alcance básico, y uso de sentencias."""

    BUILTINS: Set[str] = {"print", "len", "str", "int", "float", "bool", "list", "dict"}

    def __init__(self):
        self.errors: List[str] = []
        self.scopes: List[Dict[str, bool]] = [{}]      # pila de scopes
        self.functions: Dict[str, FunctionNode] = {}
        self.classes: Dict[str, ClassNode] = {}
        self.loop_depth: int = 0
        self.current_function: FunctionNode | None = None

    # ---- helpers de símbolos ---------------------------------------
    def _declare(self, name: str):
        self.scopes[-1][name] = True

    def _is_declared(self, name: str) -> bool:
        if name in self.BUILTINS or name in self.functions or name in self.classes:
            return True
        return any(name in s for s in reversed(self.scopes))

    # ---- entry -----------------------------------------------------
    def analyze(self, ast: ProgramNode) -> List[str]:
        self.visit(ast)
        return self.errors

    # ---- visitors --------------------------------------------------
    def visit_ProgramNode(self, node: ProgramNode):
        for stmt in node.body:
            self.visit(stmt)

    # --- declaraciones ---------------------------------------------
    def visit_FunctionNode(self, node: FunctionNode):
        if node.name in self.functions or node.name in self.classes:
            self.errors.append(f"Función o clase duplicada: '{node.name}'.")
            return
        self.functions[node.name] = node

        self.scopes.append({})
        for p in node.params:
            self._declare(p)

        prev_fn = self.current_function
        self.current_function = node
        for stmt in node.body:
            self.visit(stmt)
        self.current_function = prev_fn
        self.scopes.pop()

    def visit_ClassNode(self, node: ClassNode):
        if node.name in self.classes or node.name in self.functions:
            self.errors.append(f"Función o clase duplicada: '{node.name}'.")
            return
        self.classes[node.name] = node

        self.scopes.append({})
        for stmt in node.body:
            self.visit(stmt)
        self.scopes.pop()

    def visit_ImportNode(self, node: ImportNode):
        for mod, alias in node.names:
            self._declare(alias or mod.split(".")[0])

    # --- control de flujo ------------------------------------------
    def visit_WhileNode(self, node: WhileNode):
        self.visit(node.cond)
        self.loop_depth += 1
        self.scopes.append({})
        for stmt in node.body:
            self.visit(stmt)
        self.scopes.pop()
        self.loop_depth -= 1

    def visit_ForNode(self, node: ForNode):
        self.visit(node.iterable)
        self.loop_depth += 1
        self.scopes.append({})
        self._declare(node.target)
        for stmt in node.body:
            self.visit(stmt)
        self.scopes.pop()
        self.loop_depth -= 1

    def visit_IfNode(self, node: IfNode):
        self.visit(node.cond)
        for block in [node.body] + [b for _, b in node.elif_blocks] + ([node.else_body] if node.else_body else []):
            if block:
                self.scopes.append({})
                for stmt in block:
                    self.visit(stmt)
                self.scopes.pop()

    def visit_TryNode(self, node: TryNode):
        for stmt in node.body:
            self.visit(stmt)
        for h in node.handlers:
            self.scopes.append({})
            if h.exc and " as " in h.exc:
                alias = h.exc.split(" as ")[-1]
                self._declare(alias)
            for stmt in h.body:
                self.visit(stmt)
            self.scopes.pop()
        for block in (node.else_body or []) + (node.finally_body or []):
            self.visit(block)

    # --- sentencias simples ----------------------------------------
    def visit_ReturnNode(self, node: ReturnNode):
        if self.current_function is None:
            self.errors.append("'return' fuera de una función.")
        if node.value:
            self.visit(node.value)

    def visit_BreakNode(self, node: BreakNode):
        if self.loop_depth == 0:
            self.errors.append("'break' fuera de un bucle.")

    def visit_PassNode(self, node: PassNode):
        pass

    def visit_AssignmentNode(self, node: AssignmentNode):
        self.visit(node.value)
        self._declare(node.target)

    def visit_AugmentedAssignmentNode(self, node: AugmentedAssignmentNode):
        if not self._is_declared(node.target):
            self.errors.append(f"Variable no declarada antes de usarla: '{node.target}'.")
        self.visit(node.value)

    # --- expresiones -----------------------------------------------
    def visit_IdentifierNode(self, node: IdentifierNode):
        if not self._is_declared(node.name):
            self.errors.append(f"Identificador no declarado: '{node.name}'.")

    def visit_FunctionCallNode(self, node: FunctionCallNode):
        if node.name not in self.functions and node.name not in self.BUILTINS:
            self.errors.append(f"Llamada a función no definida: '{node.name}'.")
        for arg in node.args:
            self.visit(arg)

    def visit_MethodCallNode(self, node: MethodCallNode):
        if not self._is_declared(node.obj):
            self.errors.append(f"Objeto no declarado: '{node.obj}'.")
        for arg in node.args:
            self.visit(arg)

# ---------------------------------------------------------------------
# 2) Intérprete / Linker
# ---------------------------------------------------------------------
class _ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value

class Interpreter(NodeVisitor):
    """Ejecuta el AST tras pasar el análisis semántico."""

    BIN_OPS = {
        "+": _op.add,  "-": _op.sub, "*": _op.mul, "/": _op.truediv,
        "//": _op.floordiv, "%": _op.mod,
        "==": _op.eq, "!=": _op.ne,
        "<": _op.lt, "<=": _op.le, ">": _op.gt, ">=": _op.ge,
        "and": lambda a, b: a and b,
        "or":  lambda a, b: a or b,
    }
    UN_OPS = {
        "+": lambda x: +x,
        "-": lambda x: -x,
        "not": lambda x: not x,
    }

    def __init__(self):
        self.globals: Dict[str, Any] = {}
        self.output: List[str] = []

    # ---- helpers ---------------------------------------------------
    def _call_builtin(self, name: str, args: List[Any]):
        if name == "print":
            self.output.append(" ".join(str(a) for a in args))
            return None
        # Fallback a builtins de Python reales (seguro para este scope educativo)
        if hasattr(_py_builtins, name):
            fn = getattr(_py_builtins, name)
            return fn(*args)
        raise RuntimeError(f"Builtin '{name}' no soportado.")

    # ---- visitores -------------------------------------------------
    def visit_ProgramNode(self, node: ProgramNode):
        for stmt in node.body:
            self.visit(stmt)
        return {"output": self.output, "globals": self.globals}

    # --- declaraciones ---------------------------------------------
    def visit_FunctionNode(self, node: FunctionNode):
        # Guardamos una función Python-callback en globals
        def _fn(*args):
            local_env_backup = self.globals.copy()
            for name, val in zip(node.params, args):
                self.globals[name] = val
            try:
                for st in node.body:
                    self.visit(st)
            except _ReturnSignal as rs:
                result = rs.value
            else:
                result = None
            finally:
                self.globals = local_env_backup
            return result

        self.globals[node.name] = _fn

    def visit_ClassNode(self, node: ClassNode):
        # Implementación mínima: dict con métodos
        cls_dict: Dict[str, Any] = {}
        orig_globals = self.globals
        self.globals = cls_dict
        for stmt in node.body:
            self.visit(stmt)
        self.globals = orig_globals
        self.globals[node.name] = cls_dict

    def visit_ImportNode(self, node: ImportNode):
        for mod, alias in node.names:
            self.globals[alias or mod.split(".")[0]] = __import__(mod)

    # --- control de flujo ------------------------------------------
    def visit_IfNode(self, node: IfNode):
        if self.visit(node.cond):
            for st in node.body:
                self.visit(st)
            return
        for cond, body in node.elif_blocks:
            if self.visit(cond):
                for st in body:
                    self.visit(st)
                return
        if node.else_body:
            for st in node.else_body:
                self.visit(st)

    def visit_WhileNode(self, node: WhileNode):
        while self.visit(node.cond):
            for st in node.body:
                self.visit(st)

    def visit_ForNode(self, node: ForNode):
        iterable = self.visit(node.iterable)
        for val in iterable:
            self.globals[node.target] = val
            for st in node.body:
                self.visit(st)

    def visit_TryNode(self, node: TryNode):
        try:
            for st in node.body:
                self.visit(st)
        except Exception as e:
            handled = False
            for h in node.handlers:
                if h.exc is None or (h.exc.split()[0] == type(e).__name__):
                    if h.exc and " as " in h.exc:
                        alias = h.exc.split(" as ")[-1]
                        self.globals[alias] = e
                    for st in h.body:
                        self.visit(st)
                    handled = True
                    break
            if not handled:
                raise
        else:
            if node.else_body:
                for st in node.else_body:
                    self.visit(st)
        finally:
            if node.finally_body:
                for st in node.finally_body:
                    self.visit(st)

    # --- sentencias simples ----------------------------------------
    def visit_PassNode(self, node: PassNode):
        pass

    def visit_BreakNode(self, node: BreakNode):
        raise RuntimeError("'break' fuera de contexto soportado (no implementado).")

    def visit_ReturnNode(self, node: ReturnNode):
        value = self.visit(node.value) if node.value else None
        raise _ReturnSignal(value)

    def visit_AssignmentNode(self, node: AssignmentNode):
        self.globals[node.target] = self.visit(node.value)

    def visit_AugmentedAssignmentNode(self, node: AugmentedAssignmentNode):
        val = self.globals.get(node.target, 0)
        rhs = self.visit(node.value)
        op_fn = self.BIN_OPS.get(node.op)
        if op_fn is None:
            raise RuntimeError(f"Operador compuesto no soportado: {node.op}")
        self.globals[node.target] = op_fn(val, rhs)

    # --- expresiones -----------------------------------------------
    def visit_IdentifierNode(self, node: IdentifierNode):
        if node.name in self.globals:
            return self.globals[node.name]
        raise RuntimeError(f"Variable '{node.name}' no definida.")

    def visit_ConstantNode(self, node: ConstantNode):
        return int(node.value) if isinstance(node.value, str) and node.value.isdigit() else node.value

    def visit_StringNode(self, node: StringNode):
        return node.value.strip('"\'')

    def visit_ListNode(self, node: ListNode):
        return [self.visit(e) for e in node.elements]

    def visit_DictNode(self, node: DictNode):
        return {self.visit(k): self.visit(v) for k, v in node.pairs}

    def visit_TupleNode(self, node: TupleNode):
        return tuple(self.visit(e) for e in node.elements)

    def visit_UnaryOpNode(self, node: UnaryOpNode):
        op_fn = self.UN_OPS.get(node.op)
        if op_fn is None:
            raise RuntimeError(f"Operador unario '{node.op}' no soportado.")
        return op_fn(self.visit(node.operand))

    def visit_BinaryOpNode(self, node: BinaryOpNode):
        op_fn = self.BIN_OPS.get(node.op)
        if op_fn is None:
            raise RuntimeError(f"Operador binario '{node.op}' no soportado.")
        return op_fn(self.visit(node.left), self.visit(node.right))

    def visit_FunctionCallNode(self, node: FunctionCallNode):
        args = [self.visit(a) for a in node.args]
        if node.name in self.globals:
            return self.globals[node.name](*args)
        return self._call_builtin(node.name, args)

    def visit_MethodCallNode(self, node: MethodCallNode):
        obj = self.visit(IdentifierNode(node.obj))
        method = getattr(obj, node.method, None)
        if method is None:
            raise RuntimeError(f"Objeto no tiene método '{node.method}'.")
        args = [self.visit(a) for a in node.args]
        return method(*args)

# Alias Linker
Linker = Interpreter

# ---------------------------------------------------------------------
# 3) Función de alto nivel
# ---------------------------------------------------------------------
def link_and_run(ast: ProgramNode):
    """Realiza semántica + ejecución. Devuelve dict con salida y globals.

    Uso:
    ----
    >>> from parser import Parser   # token_list ya debe existir
    >>> ast = Parser(tokens).parse()
    >>> result = link_and_run(ast)
    >>> print(result['output'])
    """
    sem = SemanticAnalyzer()
    errs = sem.analyze(ast)
    if errs:
        return {"errors": errs}

    intrp = Interpreter()
    return intrp.visit(ast)
