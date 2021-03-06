"""CPU functionality."""

import sys
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CMP = 0b10100111
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
AND = 0b10101000
NOT = 0b01101001
OR = 0b10101010
XOR = 0b10101011
SHL = 0b10101100
SHR = 0b10101101
MOD = 0b10100100


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.pc = 0
        self.ram = [0] * 256
        self.running = True
        self.reg[7] = 0xf4
        self.sp = self.reg[7]
        self.fl = 0b00000000
        self.branchtable = {}
        self.branchtable[HLT] = self.op_hlt
        self.branchtable[LDI] = self.op_ldi
        self.branchtable[PRN] = self.op_prn
        self.branchtable[MUL] = self.op_mul
        self.branchtable[PUSH] = self.op_push
        self.branchtable[POP] = self.op_pop
        self.branchtable[CALL] = self.op_call
        self.branchtable[RET] = self.op_ret
        self.branchtable[ADD] = self.op_add
        self.branchtable[CMP] = self.op_cmp
        self.branchtable[JMP] = self.op_jmp
        self.branchtable[JEQ] = self.op_jeq
        self.branchtable[JNE] = self.op_jne
        self.branchtable[AND] = self.op_and
        self.branchtable[NOT] = self.op_not
        self.branchtable[OR] = self.op_or
        self.branchtable[XOR] = self.op_xor
        self.branchtable[SHL] = self.op_shl
        self.branchtable[SHR] = self.op_shr
        self.branchtable[MOD] = self.op_mod

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def op_hlt(self, operand_a, operand_b):
        self.running = False

    def op_ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        # self.pc += 3

    def op_prn(self, operand_a, operand_b):
        print('prn:', self.reg[operand_a])
        # self.pc += 2

    def op_mul(self, operand_a, operand_b):
        self.alu('MUL', operand_a, operand_b)
        # self.pc += 3

    def op_push(self, operand_a, operand_b):
        self.sp -= 1
        val = self.reg[operand_a]
        self.ram_write(self.sp, val)
        # self.pc += 2

    def op_pop(self, operand_a, operand_b):
        self.reg[operand_a] = self.ram_read(self.sp)
        # self.pc += 2
        self.sp += 1

    def op_call(self, operand_a, operand_b):
        ret_addr = self.pc + 2
        self.sp -= 1
        self.ram_write(self.sp, ret_addr)  # write sp and pc location to ram
        sub_addr = self.reg[operand_a]
        self.pc = sub_addr

    def op_ret(self, operand_a, operand_b):
        ret_addr = self.ram_read(self.sp)  # set ret_addr to location in ram
        self.sp += 1
        self.pc = ret_addr

    def op_add(self, operand_a, operand_b):
        self.alu('ADD', operand_a, operand_b)

    def op_cmp(self, operand_a, operand_b):
        self.alu('CMP', operand_a, operand_b)

    def op_jmp(self, operand_a, operand_b):
        self.pc = self.reg[operand_a]

    def op_jeq(self, operand_a, operand_b):
        if self.fl == 0b00000001:
            self.op_jmp(operand_a, operand_b)
        else:
            self.pc += 2

    def op_jne(self, operand_a, operand_b):
        if self.fl != 0b00000001:
            self.op_jmp(operand_a, operand_b)
        else:
            self.pc += 2

    def op_and(self, operand_a, operand_b):
        self.alu('AND', operand_a, operand_b)

    def op_or(self, operand_a, operand_b):
        self.alu('ADD', operand_a, operand_b)

    def op_xor(self, operand_a, operand_b):
        self.alu('CMP', operand_a, operand_b)

    def op_not(self, operand_a, operand_b):
        self.alu('ADD', operand_a, operand_b)

    def op_shl(self, operand_a, operand_b):
        self.alu('CMP', operand_a, operand_b)

    def op_shr(self, operand_a, operand_b):
        self.alu('ADD', operand_a, operand_b)

    def op_mod(self, operand_a, operand_b):
        self.alu('CMP', operand_a, operand_b)

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        with open(filename) as file:
            for line in file:
                val = line.split("#")[0].strip()
                if val == '':
                    continue
                instruction = int(val, 2)
                self.ram[address] = instruction
                address += 1

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

        if op == 'ADD':
            self.reg[reg_a] = self.reg[reg_a] + self.reg[reg_b]
        elif op == 'MUL':
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
        elif op == 'CMP':
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000001
        elif op == 'AND':
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
        elif op == 'OR':
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        elif op == 'XOR':
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
        elif op == 'NOT':
            self.reg[reg_a] = ~self.reg[reg_a]
        elif op == 'SHL':
            self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
        elif op == 'SHR':
            self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]
        elif op == 'MOD':
            if self.reg[reg_b] == 0:
                print('ERROR: divide by 0')
                self.op_hlt()
            else:
                remainder = self.reg[reg_a] % self.reg[reg_b]
                self.reg[reg_a] = remainder

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
        self.trace()

        while self.running is True:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # This increments the pc position automatically
            op_size = IR >> 6
            ins_set = ((IR >> 4) & 0b1) == 1
            if not ins_set:
                self.pc += op_size + 1

            if IR in self.branchtable:
                self.branchtable[IR](operand_a, operand_b)

# SAVE WHERE WE'RE COMING FROM TO THE STACK AND SET PC TO WHERE WE'RE GOING
