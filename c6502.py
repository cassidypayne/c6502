import instructions
from memory import Register, Flag, Memory


#
# CPU class. functions referenced in instructions dict operate on these.


class C6502:
    def __init__(self):
        self.acc = Register(1)
        self.x = Register(1)
        self.y = Register(1)
        self.sp = Register(1, 0xff)
        self._sp_page = 0x100  # 0x100, 0x200, 0x300, ...
        self.pc = Register(2)

        self.n = Flag()
        self.v = Flag()
        self.b = Flag()
        self.d = Flag()
        self.i = Flag(True)
        self.z = Flag()
        self.c = Flag()

        self.ram = Memory()

        self.debug = False

    def p(self, mem=None):
        p = 0x0
        if mem is None:
            flags = (self.n() << 7, self.v() << 6, 0x0, self.b() << 4,
                     self.d() << 3, self.i() << 2, self.z() << 1, self.c())
            for i in flags:
                p = p | i
            return p
        else:
            mem %= 0x100
            val = ()
            for bitpos in range(8):
                val += (mem & (0x1 << bitpos),)
            for bit in val:
                p = p | bit
            self._set_flags(p)

    def _set_flags(self, p):
        self.n(p & 0x80)
        self.v(p & 0x40)
        self.b(p & 0x20)
        self.d(p & 0x10)
        self.i(p & 0x8)
        self.z(p & 0x4)
        self.c(p & 0x1)

    def push(self, mem):  # stack
        addr = self.sp() + self._sp_page
        self.ram(addr, mem)
        self.sp(self.sp() - 1)

    def pull(self):
        self.sp(self.sp() + 1)
        addr = self.sp() + self._sp_page
        mem = self.ram(addr)
        return mem

    #
    # addressing; imp -> None, literal -> unchanged, else -> abs.

    def _addr_acc(self, mem):
        return None

    def _addr_abs(self, mem):
        return mem

    def _addr_abx(self, mem):
        return mem + self.x()

    def _addr_aby(self, mem):
        return mem + self.y()

    def _addr_imm(self, mem):
        return mem

    def _addr_imp(self, mem):
        return None

    def _addr_ind(self, mem):  # to-do: hb should loop around page
        lb = self.ram(mem)
        hb = self.ram(mem + 1)
        return (hb << 8) | lb

    def _addr_iix(self, mem):
        lb = self.ram(mem + self.x())
        hb = self.ram(mem + self.x() + 1)
        return (hb << 8) | lb

    def _addr_iiy(self, mem):
        lb = self.ram(mem)
        hb = self.ram(mem + 1)
        val = ((hb << 8) | lb) + self.y()
        return val

    def _addr_rel(self, mem):
        negative = (mem >> 7) & 0x1
        offset = 0 - (256 - mem) if negative else mem
        return self.pc() + offset

    def _addr_zpg(self, mem):
        return mem % 0x100

    def _addr_zpx(self, mem):
        return mem + self.x()

    def _addr_zpy(self, mem):
        return mem + self.y()

    addr_modes = {
        'acc': _addr_acc, 'abs': _addr_abs, 'abx': _addr_abx, 'aby': _addr_aby,
        'imm': _addr_imm, 'imp': _addr_imp, 'ind': _addr_ind, 'iix': _addr_iix,
        'iiy': _addr_iiy, 'rel': _addr_rel, 'zpg': _addr_zpg, 'zpx': _addr_zpx,
        'zpy': _addr_zpy
    }

    def _get_addr(self, mode, mem):
        return self.addr_modes[mode](self, mem)

    #
    # higher-level functions.

    def _get_bytes(self):
        opcode, arg = self.ram(self.pc()), None
        try:
            size = instructions.get_size(opcode)
        except KeyError:
            print('invalid opcode! passing NOP...')
            opcode, size = 0xea, instructions.get_size(0xea)
        if size > 1:
            lb = self.ram(self.pc() + 1)
            if size == 2:
                arg = lb
            elif size == 3:
                hb = self.ram(self.pc() + 2)
                arg = (hb << 8) | lb
        self.pc(self.pc() + size)

        return opcode, arg  # int, int

    def _prepare_instruction(self, opcode, arg):
        instruction = instructions.get_instruction(opcode)
        mode = instructions.get_mode(opcode)
        arg = self._get_addr(mode, arg)
        return instruction, mode, arg  # func, str, int

    def _execute(self, instruction, mode, arg):
        instruction(self, mode, arg)

    def step(self):
        opcode = self._get_bytes()  # advances pc
        instruction = self._prepare_instruction(*opcode)
        self._execute(*instruction)
