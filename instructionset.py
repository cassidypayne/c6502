#
# c6502.py addressing mode functions always return an absolute address or a literal;
# 'imm' or 'acc' passed as mode results in the appropriate treatment.


def ADC(cpu, mode, op):
    mem = op if mode == 'imm' else cpu.ram(op)
    val = cpu.acc() + mem + cpu.c()
    cpu.v(True if val > 0xff else False)
    cpu.n(val >> 7)
    if cpu.d():
        pass
    else:
        cpu.c(val > 0xff)
    cpu.acc(val)


def AND(cpu, mode, op):
    mem = op if mode == 'imm' else cpu.ram(op)
    val = mem & cpu.acc()
    cpu.acc(val)
    cpu.n(val >> 7)
    cpu.z(not val)


def ASL(cpu, mode, op):
    mem = cpu.acc() if mode == 'acc' else cpu.ram(op)
    val = (mem << 1) & 0xfe
    cpu.acc(val) if mode == 'acc' else cpu.ram(op, val)
    cpu.n(val >> 7)
    cpu.z(not val)
    cpu.c(mem >> 7)


def BCC(cpu, mode, op):
    if not cpu.c():
        cur_pc = cpu.pc()
        mem = (cur_pc + op) % 0x10000
        JMP(cpu, 'imm', mem)


def BCS(cpu, mode, op):
    if cpu.c():
        cur_pc = cpu.pc()
        mem = (cur_pc + op) % 0x10000
        JMP(cpu, 'imm', mem)


def BEQ(cpu, mode, op):
    if cpu.z():
        mem = op
        JMP(cpu, 'imm', mem)


def BIT(cpu, mode, op):
    mem = cpu.ram(op)
    val = cpu.acc() & mem
    cpu.n(val >> 7)
    cpu.z(not val)
    cpu.v((val >> 6) & 0x1)


def BMI(cpu, mode, op):
    if cpu.n():
        cur_pc = cpu.pc()
        mem = (cur_pc + op) % 0x10000
        JMP(cpu, 'imm', mem)


def BNE(cpu, mode, op):
    if not cpu.z():
        cur_pc = cpu.pc()
        mem = (cur_pc + op) % 0x10000
        JMP(cpu, 'imm', mem)


def BPL(cpu, mode, op):
    if not cpu.n():
        cur_pc = cpu.pc()
        mem = (cur_pc + op) % 0x10000
        JMP(cpu, 'imm', mem)


def BRK(cpu, mode, op):
    cpu.push(cpu.pc() >> 8)
    cpu.push(cpu.pc() & 0xff)
    cpu.push(cpu.p() | 0x10)
    cpu.pc((cpu.ram(0xffff) << 8) | cpu.ram(0xfffe))


def BVC(cpu, mode, op):
    if not cpu.v():
        cur_pc = cpu.pc()
        mem = (cur_pc + op) % 0x10000
        JMP(cpu, 'imm', mem)


def BVS(cpu, mode, op):
    if cpu.v():
        cur_pc = cpu.pc()
        mem = (cur_pc + op) % 0x10000
        JMP(cpu, 'imm', mem)


def CLC(cpu, mode, op):
    cpu.c(False)


def CLD(cpu, mode, op):
    cpu.d(False)


def CLI(cpu, mode, op):
    cpu.i(False)


def CLV(cpu, mode, op):
    cpu.v(False)


def CMP(cpu, mode, op):
    mem = op if mode == 'imm' else cpu.ram(op)
    val = (cpu.acc() - mem) % 0x100
    cpu.n(val >> 7)
    cpu.z(not val)
    cpu.c(cpu.acc() >= mem)


def CPX(cpu, mode, op):
    mem = op if mode == 'imm' else cpu.ram(op)
    val = (cpu.x() - mem()) % 0x100
    cpu.n(val >> 7)
    cpu.z(not val)
    cpu.c(cpu.x() >= mem)


def CPY(cpu, mode, op):
    mem = op if mode == 'imm' else cpu.ram(op)
    val = (cpu.y() - mem) % 0x100
    cpu.n(val >> 7)
    cpu.z(not val)
    cpu.c(cpu.y() >= mem)


def DEC(cpu, mode, op):
    mem = cpu.ram(op)
    val = (mem - 1) % 0x100
    cpu.ram(op, val)
    cpu.n(val >> 7)
    cpu.z(not val)


def DEX(cpu, mode, op):
    val = (cpu.x() - 1) % 0x100
    cpu.x(val)
    cpu.n(val >> 7)
    cpu.z(not val)


def DEY(cpu, mode, op):
    val = (cpu.y() - 1) % 0x100
    cpu.y(val)
    cpu.n(val >> 7)
    cpu.z(not val)


def EOR(cpu, mode, op):
    mem = op if mode == 'imm' else cpu.ram(op)
    val = cpu.acc() ^ mem
    cpu.acc(val)
    cpu.n(val >> 7)
    cpu.z(not val)


def INC(cpu, mode, op):
    mem = cpu.ram(op)
    val = (mem + 1) % 0x100
    cpu.ram(op, val)
    cpu.n(val >> 7)
    cpu.z(not val)


def INX(cpu, mode, op):
    val = cpu.x() + 1
    cpu.x(val)
    cpu.n(val >> 7)
    cpu.z(not val)


def INY(cpu, mode, op):
    val = cpu.y() + 1
    cpu.y(val)
    cpu.n(val >> 7)
    cpu.z(not val)


def JMP(cpu, mode, op):
    cpu.pc(op)


def JSR(cpu, mode, op):
    mem = (cpu.pc() + 2) % 0x10000
    meml, memh = mem & 0xff, mem << 8 & 0xff00
    cpu.push(memh)
    cpu.push(meml)
    val = cpu.ram(op)
    cpu.pc(val)


def LDA(cpu, mode, op):
    mem = op if mode == 'imm' else cpu.ram(op)
    cpu.acc(mem)
    cpu.n(mem >> 7)
    cpu.z(not mem)


def LDX(cpu, mode, op):
    mem = op if mode == 'imm' else cpu.ram(op)
    cpu.x(mem)
    cpu.n(mem >> 7)
    cpu.z(not mem)


def LDY(cpu, mode, op):
    mem = op if mode == 'imm' else cpu.ram(op)
    cpu.y(mem)
    cpu.n(mem >> 7)
    cpu.z(not mem)


def LSR(cpu, mode, op):
    mem = cpu.ram(op) if mode != 'acc' else cpu.acc()
    cpu.n(False)
    cpu.c(mem & 0x1)
    val = mem >> 1
    cpu.z(not val)
    if mode != 'acc':
        cpu.ram(op, val)
    else:
        cpu.acc(val)


def NOP(cpu, mode, op):
    pass


def ORA(cpu, mode, op):
    mem = op if mode == 'imm' else cpu.ram(op)
    val = cpu.acc() | mem
    cpu.acc(val)
    cpu.n(val >> 7)
    cpu.z(not val)


def PHA(cpu, mode, op):
    cpu.push(cpu.acc())


def PHP(cpu, mode, op):
    cpu.push(cpu.p())


def PLA(cpu, mode, op):
    mem = cpu.pull()
    cpu.acc(mem)
    cpu.n(mem >> 7)
    cpu.z(not mem)


def PLP(cpu, mode, op):
    mem = cpu.pull()
    cpu.p(mem)


def ROL(cpu, mode, op):
    mem = cpu.acc() if mode == 'acc' else cpu.ram(op)
    val = mem >> 7
    mem = (mem << 1) | cpu.c()
    if mode == 'acc':
        cpu.acc(mem)
    else:
        cpu.ram(op, mem)
    cpu.c(val)
    cpu.z(not mem)
    cpu.n(mem >> 7)


def ROR(cpu, mode, op):
    mem = cpu.acc() if mode == 'acc' else cpu.ram(op)
    val = mem & 0x1
    mem = (mem >> 1) | cpu.c()
    if mode == 'acc':
        cpu.acc(mem)
    else:
        cpu.ram(op, mem)
    cpu.c(val)
    cpu.z(not mem)
    cpu.n(mem >> 7)


def RTI(cpu, mode, op):
    cpu.p(cpu.pull())
    lo = cpu.pull()
    hi = cpu.pull()
    cpu.pc((hi << 8) | lo)


def RTS(cpu, mode, op):
    meml = cpu.pull()
    memh = cpu.pull()
    mem = (memh << 8) | meml
    cpu.pc(mem)


def SBC(cpu, mode, op):
    mem = op if mode == 'imm' else cpu.ram(op)
    if cpu.d():
        pass
    else:
        val = cpu.acc() - mem - (not cpu.c())
        cpu.v((val > 127) or (val < -128))


def SEC(cpu, mode, op):
    cpu.c(True)


def SED(cpu, mode, op):
    cpu.d(True)


def SEI(cpu, mode, op):
    cpu.i(True)


def STA(cpu, mode, op):
    mem = cpu.acc()
    cpu.ram(op, mem)


def STX(cpu, mode, op):
    mem = cpu.x()
    cpu.ram(op, mem)


def STY(cpu, mode, op):
    mem = cpu.y()
    cpu.ram(op, mem)


def TAX(cpu, mode, op):
    mem = cpu.acc()
    cpu.x(mem)
    cpu.n(mem << 7)
    cpu.z(not mem)


def TAY(cpu, mode, op):
    mem = cpu.acc()
    cpu.y(mem)
    cpu.n(mem << 7)
    cpu.z(not mem)


def TSX(cpu, mode, op):
    mem = cpu.sp()
    cpu.x(mem)
    cpu.n(mem << 7)
    cpu.z(not mem)


def TXA(cpu, mode, op):
    mem = cpu.x()
    cpu.acc(mem)
    cpu.n(mem << 7)
    cpu.z(not mem)


def TXS(cpu, mode, op):
    mem = cpu.x()
    cpu.sp(mem)


def TYA(cpu, mode, op):
    mem = cpu.y()
    cpu.acc(mem)
    cpu.n(mem << 7)
    cpu.z(not mem)
