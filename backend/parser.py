
# ---------------------------------------------------------------------------
#  TOKENS
# ---------------------------------------------------------------------------

class Token:
    def __init__(self, type_, value):
        self.type  = type_
        self.value = value
    def __repr__(self):
        return f"Token({self.type}, {self.value})"

# ---------------------------------------------------------------------------
#  AST NODES
# ---------------------------------------------------------------------------

class ASTNode: ...

class ProgramNode(ASTNode):
    def __init__(self, body):  self.body = body


# --- sentencias ------------------------------------------------------------

class FunctionNode(ASTNode):
    def __init__(self, name, params, body):
        self.name, self.params, self.body = name, params, body

class ClassNode(ASTNode):
    def __init__(self, name, body):
        self.name, self.body = name, body

class ImportNode(ASTNode):
    def __init__(self, names):  # [(módulo, alias)]
        self.names = names

class WhileNode(ASTNode):
    def __init__(self, cond, body):
        self.cond, self.body = cond, body

class ForNode(ASTNode):
    def __init__(self, target, iterable, body):
        self.target, self.iterable, self.body = target, iterable, body

class IfNode(ASTNode):
    def __init__(self, cond, body, elif_blocks=None, else_body=None):
        self.cond = cond
        self.body = body
        self.elif_blocks = elif_blocks or []   # [(cond, body)]
        self.else_body   = else_body


class TryNode(ASTNode):
    def __init__(self, body, handlers, else_body=None, finally_body=None):
        self.body = body
        self.handlers = handlers
        self.else_body = else_body
        self.finally_body = finally_body


class ExceptHandlerNode(ASTNode):
    def __init__(self, exc, body):
        self.exc, self.body = exc, body

class PassNode(ASTNode): ...
class BreakNode(ASTNode): ...

class ReturnNode(ASTNode):
    def __init__(self, value): self.value = value

class AssignmentNode(ASTNode):
    def __init__(self, target, value):
        self.target, self.value = target, value


class AugmentedAssignmentNode(ASTNode):
    def __init__(self, target, op, value):
        self.target, self.op, self.value = target, op, value
class ObjectInstanceNode(ASTNode):
    def __init__(self, name, klass): self.name, self.klass = name, klass

# --- expresiones -----------------------------------------------------------

class IdentifierNode(ASTNode):
    def __init__(self, name): self.name = name

class ConstantNode(ASTNode):
    def __init__(self, value): self.value = value

class StringNode(ASTNode):
    def __init__(self, value): self.value = value

class ListNode(ASTNode):
    def __init__(self, elements): self.elements = elements

class DictNode(ASTNode):
    def __init__(self, pairs): self.pairs = pairs  # list of (key,val)

class TupleNode(ASTNode):
    def __init__(self, elements): self.elements = elements

class UnaryOpNode(ASTNode):
    def __init__(self, op, operand):
        self.op, self.operand = op, operand

class BinaryOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left, self.op, self.right = left, op, right

class FunctionCallNode(ASTNode):
    def __init__(self, name, args): self.name, self.args = name, args

class MethodCallNode(ASTNode):
    def __init__(self, obj, method, args): self.obj, self.method, self.args = obj, method, args

# ---------------------------------------------------------------------------
#  PARSER
# ---------------------------------------------------------------------------

class Parser:
    AUG_ASSIGN_OPS = {'+=', '-=', '*=', '/=', '//=', '%=', '**=', '&=', '|=', '^=', '>>=', '<<='}
    def __init__(self, token_list):
        self.tokens = [Token(t['type'], t['value']) for t in token_list]
        self.pos = 0

    # ---------- helpers ----------------------------------------------------

    def cur(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else Token('EOF','')
    def look(self, n=1):
        idx = self.pos + n
        return self.tokens[idx] if idx < len(self.tokens) else Token('EOF','')

    def consume(self, ttype=None, value=None):
        tok = self.cur()
        if ttype and tok.type != ttype:
            raise SyntaxError(f"Esperaba {ttype}, obtuve {tok.type}:{tok.value}")
        if value and tok.value != value:
            raise SyntaxError(f"Esperaba '{value}', obtuve '{tok.value}'")
        self.pos += 1
        return tok

    # ---------- entry ------------------------------------------------------

    def parse(self):
        body=[]
        while self.cur().type != 'EOF':
            body.append(self.parse_stmt())
        return ProgramNode(body)

    # ---------- statements -------------------------------------------------

    def parse_stmt(self):
        tok=self.cur()

        if tok.type=='KEYWORD':
            kw=tok.value
            if kw=='def':   return self.parse_function()
            if kw=='class': return self.parse_class()
            if kw=='import':return self.parse_import()
            if kw=='if':    return self.parse_if()
            if kw=='while': return self.parse_while()
            if kw=='for':   return self.parse_for()
            if kw=='try':   return self.parse_try()
            if kw=='pass':
                self.consume('KEYWORD','pass'); return PassNode()
            if kw=='break':   return self.consume('KEYWORD','break') or BreakNode()
            if kw=='return':
                self.consume('KEYWORD','return')
                val = self.parse_expr()
                return ReturnNode(val)

        if tok.type=='IDENTIFIER':
            # obj.meth(...)
            if self.look().value=='.':
                obj=self.consume('IDENTIFIER').value
                self.consume('PUNCTUATION','.')
                meth=self.consume('IDENTIFIER').value
                args=self.parse_call_args()
                return MethodCallNode(obj,meth,args)
            # assign or instantiation
            

            # assignment simple o compuesto
            next_tok = self.look()
            if next_tok.value == '=' or (
                next_tok.type == 'OPERATOR' and next_tok.value in self.AUG_ASSIGN_OPS
            ):
                target = self.consume('IDENTIFIER').value
                # '=' o combinados como '+=', '-=', etc.
                op_token = self.consume('OPERATOR').value
                if op_token == '=':
                    value = self.parse_expr()
                    return AssignmentNode(target, value)
                else:
                    op = op_token[:-1]  # '+=' -> '+'
                    value = self.parse_expr()
                    return AugmentedAssignmentNode(target, op, value)
            if self.look().value=='(':
                name=self.consume('IDENTIFIER').value
                args=self.parse_call_args()
                return FunctionCallNode(name,args)

        raise SyntaxError(f"Sentencia no reconocida a partir de {tok.type}:{tok.value}")

    # ---------- skip util --------------------------------------------------

    def skip_parens(self):
        depth=1
        while depth and self.cur().type!='EOF':
            if self.cur().value=='(': depth+=1
            elif self.cur().value==')': depth-=1
            self.consume()

    # ---------- import -----------------------------------------------------

    def parse_import(self):
        self.consume('KEYWORD','import')
        names=[]
        while True:
            parts=[self.consume('IDENTIFIER').value]
            while self.cur().value=='.':
                self.consume('PUNCTUATION','.')
                parts.append(self.consume('IDENTIFIER').value)
            module='.'.join(parts)
            alias=None
            if self.cur().type=='KEYWORD' and self.cur().value=='as':
                self.consume('KEYWORD','as')
                alias=self.consume('IDENTIFIER').value
            names.append((module,alias))
            if self.cur().value==',':
                self.consume('PUNCTUATION',',')
            else:
                break
        return ImportNode(names)

    # ---------- try / except ----------------------------------------------


    def parse_try(self):
        self.consume('KEYWORD','try')
        self.consume('PUNCTUATION',':')
        body = self.parse_block(stop={'except','else','finally'})
        handlers = []
        while self.cur().type == 'KEYWORD' and self.cur().value == 'except':
            self.consume('KEYWORD','except')
            exc = None
            if self.cur().type == 'IDENTIFIER':
                exc = self.consume('IDENTIFIER').value
                if self.cur().type == 'KEYWORD' and self.cur().value == 'as':
                    self.consume('KEYWORD','as')
                    alias = self.consume('IDENTIFIER').value
                    exc += f' as {alias}'
            self.consume('PUNCTUATION',':')
            hbody = self.parse_block(stop={'except','else','finally'})
            handlers.append(ExceptHandlerNode(exc, hbody))
    
        else_body = None
        if self.cur().type == 'KEYWORD' and self.cur().value == 'else':
            self.consume('KEYWORD','else')
            self.consume('PUNCTUATION',':')
            else_body = self.parse_block(stop={'finally'})
    
        finally_body = None
        if self.cur().type == 'KEYWORD' and self.cur().value == 'finally':
            self.consume('KEYWORD','finally')
            self.consume('PUNCTUATION',':')
            finally_body = self.parse_block()
    
        return TryNode(body, handlers, else_body, finally_body)
    
    # ---------- defs -------------------------------------------------------

    def parse_function(self):
        self.consume('KEYWORD','def')
        name=self.consume('IDENTIFIER').value
        self.consume('PUNCTUATION','(')
        params=[]
        while self.cur().value!=')':
            params.append(self.consume('IDENTIFIER').value)
            if self.cur().value==',':
                self.consume('PUNCTUATION',',')
        self.consume('PUNCTUATION',')')
        self.consume('PUNCTUATION',':')
        body=self.parse_block()
        return FunctionNode(name,params,body)

    def parse_class(self):
        self.consume('KEYWORD','class')
        name=self.consume('IDENTIFIER').value
        if self.cur().value=='(':
            self.skip_parens()
        self.consume('PUNCTUATION',':')
        body=self.parse_block()
        return ClassNode(name,body)

    # ---------- control flow ----------------------------------------------

    def parse_if(self):
        self.consume('KEYWORD','if')
        cond=self.parse_expr()
        self.consume('PUNCTUATION',':')
        body=self.parse_block(stop={'elif','else'})
        elif_blocks=[]
        while self.cur().type=='KEYWORD' and self.cur().value=='elif':
            self.consume('KEYWORD','elif')
            econd=self.parse_expr()
            self.consume('PUNCTUATION',':')
            ebody=self.parse_block(stop={'elif','else'})
            elif_blocks.append((econd,ebody))
        else_body=None
        if self.cur().type=='KEYWORD' and self.cur().value=='else':
            self.consume('KEYWORD','else')
            self.consume('PUNCTUATION',':')
            else_body=self.parse_block()
        return IfNode(cond,body,elif_blocks,else_body)

    def parse_while(self):
        self.consume('KEYWORD','while')
        cond=self.parse_expr()
        self.consume('PUNCTUATION',':')
        body=self.parse_block()
        return WhileNode(cond,body)

    def parse_for(self):
        self.consume('KEYWORD','for')
        target=self.consume('IDENTIFIER').value
        self.consume('KEYWORD','in')
        iterable=self.parse_expr()
        self.consume('PUNCTUATION',':')
        body=self.parse_block()
        return ForNode(target,iterable,body)

    # ---------- générico de bloque ----------------------------------------

    def parse_block(self, stop=None):
        stop=stop or set()
        stmts=[]
        while self.cur().type!='EOF':
            if self.cur().type=='KEYWORD' and self.cur().value in stop:
                break
            # heurística de dedent
            if self.cur().type=='KEYWORD' and self.cur().value in {'def','class','if','for','while','try','import'} and stmts:
                break
            stmts.append(self.parse_stmt())
        return stmts

    # ---------- call args --------------------------------------------------

    def parse_call_args(self):
        self.consume('PUNCTUATION','(')
        args=[]
        while self.cur().value!=')':
            args.append(self.parse_expr())
            if self.cur().value==',':
                self.consume('PUNCTUATION',',')
        self.consume('PUNCTUATION',')')
        return args

    # ---------- expresiones ------------------------------------------------

    BIN_OPS = {'+','-','*','/','//','%','==','!=','<','>','<=','>=','%'}
    def parse_expr(self):
        """Parse binary expressions with left-associativity.
        Soporta operadores binarios en BIN_OPS, lógicos 'and'/'or', y el operador de pertenencia 'in'.
        """
        left = self.parse_term()
        while True:
            tok = self.cur()
            if tok.type == 'OPERATOR' and tok.value in self.BIN_OPS:
                op = tok.value
                self.consume('OPERATOR')
            elif tok.type == 'KEYWORD' and tok.value in {'and', 'or', 'in'}:
                op = tok.value
                self.consume('KEYWORD')
            else:
                break
            right = self.parse_term()
            left = BinaryOpNode(left, op, right)
        return left
    def parse_term(self):
        tok=self.cur()

        # ---------------- unario -----------------
        # literales True / False / None
        if tok.type=='KEYWORD' and tok.value in {'True','False','None'}:
            lit = {'True': True, 'False': False, 'None': None}[tok.value]
            self.consume('KEYWORD')
            return ConstantNode(lit)
        if tok.type=='KEYWORD' and tok.value=='not':
            self.consume('KEYWORD','not')
            operand = self.parse_term()
            return UnaryOpNode('not', operand)

        if tok.type=='OPERATOR' and tok.value in {'+','-'}:
            op=self.consume('OPERATOR').value
            operand=self.parse_term()
            return UnaryOpNode(op,operand)

        # ---------------- literales/ident -----------------
        if tok.type=='CONSTANT':
            return ConstantNode(self.consume('CONSTANT').value)
        if tok.type=='LITERAL':
            return StringNode(self.consume('LITERAL').value)
        if tok.type=='IDENTIFIER':
            name=self.consume('IDENTIFIER').value
            if self.cur().value=='(':
                args=self.parse_call_args()
                return FunctionCallNode(name,args)
            return IdentifierNode(name)

        # ---------------- estructuras -----------------
        if tok.value=='[':
            self.consume('PUNCTUATION','[')
            elems=[]
            while self.cur().value!=']':
                elems.append(self.parse_expr())
                if self.cur().value==',':
                    self.consume('PUNCTUATION',',')
            self.consume('PUNCTUATION',']')
            return ListNode(elems)

        if tok.value=='{':
            self.consume('PUNCTUATION','{')
            pairs=[]
            if self.cur().value!='}':
                while True:
                    key=self.parse_expr()
                    self.consume('PUNCTUATION',':')
                    val=self.parse_expr()
                    pairs.append((key,val))
                    if self.cur().value==',':
                        self.consume('PUNCTUATION',',')
                    else:
                        break
            self.consume('PUNCTUATION','}')
            return DictNode(pairs)

        if tok.value=='(':
            self.consume('PUNCTUATION','(')
            elem=self.parse_expr()
            if self.cur().value==',':
                elems=[elem]
                while self.cur().value==',':
                    self.consume('PUNCTUATION',',')
                    if self.cur().value==')': break
                    elems.append(self.parse_expr())
                self.consume('PUNCTUATION',')')
                return TupleNode(elems)
            self.consume('PUNCTUATION',')')
            return elem

        raise SyntaxError(f"Expresión inesperada en {tok.type}:{tok.value}")
