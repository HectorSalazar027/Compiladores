class SimpleAssembler:
    def __init__(self):
        self.labels = {}
        self.instructions = []
        self.output = []
        self.arg_counts = {
            "MOV": 2,
            "ADD": 2,
            "SUB": 2,
            "MUL": 2,
            "DIV": 2,
            "AND": 2,
            "OR": 2,
            "CMP": 2,
            "JMP": 1,
            "JNE": 1,
            "PRINT": 1,
            "NOT": 1,
            "HALT": 0
        }
        self.valid_registers = {
            "A", "B", "C", "D", "E", "H", "L",
            "AF", "BC", "DE", "HL", "IX", "IY", "SP", "PC"
        }
        self.register_sizes = {
            "A": 8, "B": 8, "C": 8, "D": 8, "E": 8, "H": 8, "L": 8,
            "AF": 16, "BC": 16, "DE": 16, "HL": 16, "IX": 16,
            "IY": 16, "SP": 16, "PC": 16
        }

        self.registers = {reg: 0 for reg in self.valid_registers}

    def parse(self, code):
        lines = code.strip().splitlines()
        for idx, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith(";"):
                continue
            if ":" in line:
                label = line.replace(":", "").strip()
                self.labels[label] = len(self.instructions)
            else:
                self.instructions.append(line)

    def _is_valid_register(self, name):
        return name in self.valid_registers

    def validate_instruction(self, instr, args, pc):
        expected = self.arg_counts.get(instr)
        if expected is None:
            raise ValueError(f"Instrucción desconocida: '{instr}' en línea {pc + 1}")
        if len(args) != expected:
            raise ValueError(f"{instr} espera {expected} argumento(s), pero recibió {len(args)} en línea {pc + 1}")

        if instr == "DIV":
            val2 = self._get_value(args[1])
            if val2 == 0:
                raise ValueError(f"División por cero en línea {pc + 1}")

        if instr in {"MOV", "ADD", "SUB", "MUL", "DIV", "AND", "OR", "NOT"}:
            dest = args[0].rstrip(",")
            if not self._is_valid_register(dest):
                raise ValueError(f"'{dest}' no es un registro válido en la instrucción '{instr}' en línea {pc + 1}")

        if instr in {"JMP", "JNE"}:
            label = args[0]
            if label not in self.labels:
                raise ValueError(f"Etiqueta no definida: '{label}' en línea {pc + 1}")
            
        # Verificar compatibilidad de tamaño si ambos son registros
        if instr in {"MOV", "ADD", "SUB", "MUL", "DIV", "AND", "OR"}:
            dest = args[0].rstrip(",")
            src = args[1]
            if src in self.valid_registers:
                size_dest = self.register_sizes[dest]
                size_src = self.register_sizes[src]
                if size_dest != size_src:
                    raise ValueError(
                        f"Incompatibilidad de tamaños: '{dest}' es de {size_dest} bits y '{src}' es de {size_src} bits en línea {pc + 1}"
                    )

    def execute(self):
        pc = 0
        while pc < len(self.instructions):
            parts = self.instructions[pc].split()
            instr = parts[0]
            args = parts[1:] if len(parts) > 1 else []

            self.validate_instruction(instr, args, pc)

            if instr == "MOV":
                reg_dest = args[0].rstrip(",")
                val_src = args[1]
                self.registers[reg_dest] = self._get_value(val_src)

            elif instr == "CMP":
                reg, val = args[0].rstrip(","), args[1]
                self.last_cmp = self.registers[reg] - self._get_value(val)

            elif instr == "JNE":
                label = args[0]
                if self.last_cmp != 0:
                    pc = self.labels[label]
                    continue

            elif instr == "JMP":
                label = args[0]
                pc = self.labels[label]
                continue

            elif instr == "PRINT":
                val = args[0]
                self.output.append(str(self._get_value(val)))

            elif instr == "ADD":
                reg1 = args[0].rstrip(",")
                reg2 = args[1]
                self.registers[reg1] += self._get_value(reg2)

            elif instr == "SUB":
                reg1 = args[0].rstrip(",")
                reg2 = args[1]
                self.registers[reg1] -= self._get_value(reg2)

            elif instr == "MUL":
                reg1 = args[0].rstrip(",")
                reg2 = args[1]
                self.registers[reg1] *= self._get_value(reg2)

            elif instr == "DIV":
                reg1 = args[0].rstrip(",")
                reg2 = args[1]
                self.registers[reg1] //= self._get_value(reg2)

            elif instr == "AND":
                reg1 = args[0].rstrip(",")
                reg2 = args[1]
                self.registers[reg1] &= self._get_value(reg2)

            elif instr == "OR":
                reg1 = args[0].rstrip(",")
                reg2 = args[1]
                self.registers[reg1] |= self._get_value(reg2)

            elif instr == "NOT":
                reg = args[0]
                self.registers[reg] = ~self.registers[reg]

            elif instr == "HALT":
                break

            pc += 1

    def _get_value(self, v):
        if v.lstrip("-").isdigit():
            return int(v)
        if v not in self.valid_registers:
            raise ValueError(f"Registro inválido o no permitido: '{v}'")
        return self.registers[v]

    def run(self, code):
        self.parse(code)
        self.execute()
        return {
            "registers": self.registers,
            "output": self.output
        }
