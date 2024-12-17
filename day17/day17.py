import sys

class Machine:
    def __init__(self, lines):
        for line in lines[:3]:
            parts = line.strip().split(": ")
            reg = parts[0][9]
            val = int(parts[1])
            if reg == "A":
                self.a = val
            elif reg == "B":
                self.b = val
            elif reg == "C":
                self.c = val
            else:
                raise ValueError(f"Received an unknown register {reg}: {line.strip()}")

        prog = lines[-1].strip()[9:]
        parts = prog.split(",")
        self.prog = [int(p) for p in parts]
        self.ip = 0

        self.output = []

    def __str__(self):
        return f"Reg A: {self.a}\nReg B: {self.b}\nReg C: {self.c}\nProgram: {self.prog}\nOutput is ^{','.join(self.output)}$"
    def __repr__(self):
        return self.__str__()

    def self_replicating(self):
        return [int(p) for p in self.output] == self.prog

    def execute(self):
        while True:
            opcode, operand = self.prog[self.ip], self.prog[self.ip+1]
            ptr = self.op(opcode, operand, self.ip)
            self.ip = ptr
            if self.ip+1 >= len(self.prog):
                #print(f"Can't execute instructions at {self.ip}, {self.ip+1} for prog of len {len(self.prog)}")
                return

    def _combo(self, code):
        if code in [0, 1, 2, 3]:
            return code
        elif code == 4:
            return self.a
        elif code == 5:
            return self.b
        elif code == 6:
            return self.c
        raise ValueError(f"Received invalid operand {code}")

    def op(self, opcode, operand, ptr):
        ptr = ptr + 2
        if opcode == 0:
            self.adv(self._combo(operand))
        elif opcode == 1:
            self.bxl(operand)
        elif opcode == 2:
            self.bst(self._combo(operand))
        elif opcode == 3:
            ptr = self.jnz(operand, ptr)
        elif opcode == 4:
            self.bxc(operand)
        elif opcode == 5:
            self.out(self._combo(operand))
        elif opcode == 6:
            self.bdv(self._combo(operand))
        elif opcode == 7:
            self.cdv(self._combo(operand))
        return ptr

    def adv(self, operand):
        print(f"Performing {self.a} / 2**{operand}")
        self.a = self.a // 2**operand
        print(f"Result is {self.a}")

    def bxl(self, operand):
        print(f"Performing {self.b} ^ {operand}")
        self.b = self.b ^ operand
        print(f"Result is {self.b}")

    def bst(self, operand):
        print(f"Performing {operand} % 8")
        self.b = operand % 8
        print(f"Result is {self.b}")

    def jnz(self, operand, ptr):
        if self.a == 0:
            print(f"Setting IP to {ptr} (noop)")
            return ptr
        print(f"Setting IP to {operand} (jmp)")
        return operand

    def bxc(self, operand):
        print(f"Performing {self.b} ^ {self.c}")
        self.b = self.b ^ self.c
        print(f"Result is {self.b}")

    def out(self, operand):
        print(f"Outputting {operand} % 8 = {operand%8}")
        self.output.append(str(operand % 8))

    def bdv(self, operand):
        print(f"Performing {self.a} / 2**{operand}")
        self.b = self.a // 2**operand
        print(f"Result is {self.b}")

    def cdv(self, operand):
        print(f"Performing {self.a} / 2**{operand}")
        self.c = self.a // 2**operand
        print(f"Result is {self.c}")



with open("d17_input.txt", "r") as f:
#with open("d17_test.txt", "r") as f:
#with open("d17_test2.txt", "r") as f:
    lines = f.readlines()

#for i in range(sys.maxsize):
#    if i%500 == 0:
#        print(f"Up to {i}")
i = 117440
m = Machine(lines)
m.a = i
m.execute()
if m.self_replicating():
    print(f"Found a self replicator! Register A should be {i}")
    print(f"After execution with {i}: {','.join(m.output)}")
    #break
print(f"After execution with {i}: {','.join(m.output)}")
