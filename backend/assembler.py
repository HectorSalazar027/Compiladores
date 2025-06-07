class SimpleAssembler:
    def __init__(self):
        self.registers = {}
        self.labels = {}
        self.instructions = []
        self.output = []

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

    def execute(self):
        pc = 0
        while pc < len(self.instructions):
            parts = self.instructions[pc].split()
            instr = parts[0]
            args = parts[1:] if len(parts) > 1 else []

            if instr == "MOV":
                reg, val = args[0].rstrip(","), args[1]
                self.registers[reg] = self._get_value(val)
            elif instr == "CMP":
                reg, val = args[0].rstrip(","), args[1]
                self.last_cmp = self.registers.get(reg, 0) - self._get_value(val)
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
            pc += 1

    def _get_value(self, v):
        return int(v) if v.isdigit() else self.registers.get(v, 0)

    def run(self, code):
        self.parse(code)
        self.execute()
        return {
            "registers": self.registers,
            "output": self.output
        }
