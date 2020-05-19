"""CPU functionality."""

import sys
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.pc = 0
        self.ram = [0] * 256
        self.running = True
        self.branchtable = {}
        self.branchtable[HLT] = self.op_hlt
        self.branchtable[LDI] = self.op_ldi
        self.branchtable[PRN] = self.op_prn
        self.branchtable[MUL] = self.op_mul

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, value, MDR):
        self.ram[MAR] = MDR

    def op_hlt(self, operand_a, operand_b):
        self.pc += 1
        self.running = False
        # sys.exit(1)

    def op_ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        self.pc += 3

    def op_prn(self, operand_a):
        print('prn:', self.reg[operand_a])
        self.pc += 2

    def op_mul(self, operand_a, operand_b):
        print(operand_a)
        print(operand_b)
        self.reg[operand_a] = self.reg[operand_a] * self.reg[operand_b]
        self.pc += 3

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        with open(filename) as file:
            for line in file:
                val = line.split("#")[0].strip()
                if val == '':
                    continue
                instruction = int(val, 2)
                # print(instruction)
                self.ram[address] = instruction
                address += 1
                # print(address)

                # if string_val == '':
                #     continue
                # else

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # HLT = 0b00000001
        # LDI = 0b10000010
        # PRN = 0b01000111
        # MUL = 0b10100010

        # self.trace()

        while self.running is True:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            op_size = IR >> 6

            # ins_set = ((IR >> 4) & 0b1) == 1

            # if IR in self.branchtable:
            #     self.branchtable[IR](operand_a, operand_b)

            # if not ins_set:
            #     print('op_size', op_size)
            #     self.pc += op_size + 1

            # if IR == LDI:
            #     self.reg[operand_a] = operand_b
            #     self.pc += 3
            # elif IR == PRN:
            #     print(self.reg[operand_a])
            #     self.pc += 2
            # elif IR == MUL:
            #     self.reg[operand_a] = self.reg[operand_a] * self.reg[operand_b]
            #     self.pc += 3
            # elif IR == HLT:
            #     self.pc += 1
            #     self.running = False
            # else:
            #     print('error')
            #     sys.exit(1)
