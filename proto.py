from c6502 import C6502

#
# globals

cpu = C6502()
cur_addr = 0x0
reg_names = ('acc', 'x', 'y', 'sp', 'pc', 'p')
flg_names = 'nv-bdizc'


#
# commands. int in, str out (except writebytestr).


def jumpto(addr):
    global cur_addr
    cur_addr = addr % 0x10000


def step():
    cpu.step()


def reset():
    global cpu
    cpu = C6502()

reg = {
    'acc': cpu.acc,
    'x': cpu.x,
    'y': cpu.y,
    'sp': cpu.sp,
    'pc': cpu.pc,
    'p': cpu.p
}


def preg(name, mem=None):
    func = reg[name]
    if mem is None:
        val = func()
        return '#%s <- %s' % (hex(val), name)
    else:
        func(mem)
        val = func()
        return '#%s -> %s (%s)' % (hex(mem), name, hex(val))


def pram(addr=None, mem=None):
    if addr is None:
        addr = cur_addr
    if mem is None:
        val = cpu.ram(addr)
        return '#%s <- %s' % (hex(val), hex(addr))
    else:
        cpu.ram(addr, mem)
        val = cpu.ram(addr)
        return '#%s -> %s (%s)' % (hex(mem), hex(addr), hex(val))


def dumpram(stop=None):
    global cur_addr
    out = ''
    if not stop:
        cur_addr += 1
        return pram(cur_addr - 1)
    for addr in range(cur_addr, stop):
        out += pram(addr) + '\n'
    return out


def dumpregs():
    out = ''
    registers = (cpu.acc(), cpu.x(), cpu.y(), cpu.sp(), cpu.pc(), cpu.p())
    vals = map(hex, registers)
    zipped = zip(reg_names, vals)
    joined = [x[0] + ' ' + x[1] + ' ' for x in zipped]
    for w in joined:
        out += w
    return out


def dumpflags():
    out = ''
    raw = bin(cpu.p())[2:]
    padded_raw = '0' * (8 - len(raw)) + raw
    formatted = ''
    for letter, bit in zip(flg_names, padded_raw):
        if bit == '1':
            formatted += letter.upper()
        else:
            formatted += letter.lower()
    out = padded_raw + ' ' + formatted
    return out


def writebytestr(mem):  # special case: type(mem) == 'str'
    global cur_addr
    out = ''
    mem = mem.replace(' ', '')
    if mem[:2] == '0x':
        mem = mem[2:]
    elif len(mem) % 2:
        mem = mem[:-1]
    for byte_index in range(0, len(mem) - 1, 2):
        byte = mem[byte_index] + mem[byte_index + 1]
        pram(cur_addr, int(byte, 16))
        out += '#' + hex(int(byte, 16)) + ' -> ' + hex(cur_addr) + '\n'
        cur_addr = (cur_addr + 1) % 0x10000
    return out


cmds = {
    'step': (step,),
    'reset': (reset,),
    'cc': (jumpto,),
    'mem': (pram,),
    'acc': (preg, 'acc'),
    'x': (preg, 'x'),
    'y': (preg, 'y'),
    'p': (preg, 'p'),
    'sp': (preg, 'sp'),
    'pc': (preg, 'pc'),
    'dmp': (dumpram,),
    'reg': (dumpregs,),
    'flg': (dumpflags,),
    'wri': writebytestr,
}


def process(str_in):
    cmd_pkg = ()

    if len(str_in) == 0:
        return 'pass',
    if 'exit' in str_in:
        return 'exit',
    if 'wri' in str_in:
        return '!!!', 'bad input'
    str_in = str_in.strip().split()
    cmd_size = len(str_in)

    if cmd_size == 2:
        try:
            str_in[1] = int(str_in[1], 16)
        except ValueError:
            return '!!!', 'bad input'
    elif cmd_size == 3:
        try:
            str_in[1] = int(str_in[1], 16)
            str_in[2] = int(str_in[2], 16)
        except ValueError:
            return '!!!', 'bad input'
    elif cmd_size != 1:
        return '!!!', 'bad input'
    if str_in[0] not in cmds.keys():
        try:
            int(str_in[0], 16)
            bytestr_in = str_in[0]
            return [cmds['wri'], bytestr_in]
        except ValueError:
            return '!!!', 'bad input'

    cmd_func = cmds[str_in[0]]
    cmd_pkg += cmd_func
    if cmd_size > 1:
        cmd_pkg += tuple(str_in[1:])

    return cmd_pkg


if __name__ == '__main__':
    print('hello')

    while True:
        try:
            str_in = input(hex(cur_addr).rstrip('L') + '> ')
        except EOFError:
            print('goodbye')
            break
        cmd_pkg = process(str_in)
        if 'exit' in cmd_pkg:
            print('goodbye')
            break
        elif '!!!' in cmd_pkg:
            print('%s...' % cmd_pkg[1])
        elif 'pass' in cmd_pkg:
            pass
        else:
            cmd = cmd_pkg[0]
            args = cmd_pkg[1:]
            output = cmd(*args)
            if output:
                print(output.strip())
            pass
