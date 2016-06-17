from c6502 import C6502
from collections import namedtuple

#
# simple debugger / memory editor for c6502.

cpu = C6502()
cur_addr = 0x0
reg_names = ('acc', 'x', 'y', 'sp', 'pc', 'p')
flg_names = 'nv-bdizc'

def hexf(i, l=2):
    return '0x' + hex(i)[2:].zfill(l)


#
# commands.

def load_file(*args): # filename, addr
    pass


def jumpto(*args): # addr
    global cur_addr

    if not len(args):
        addr = 0x0
    elif type(args[0]) is str:
        addr = int(args[0], base=16) % 0x10000
    elif type(args[0]) is int:
        addr = args[0] % 0x10000

    cur_addr = addr


def step(*args):
    cpu.step()


def reset(*args):
    global cpu
    cpu = C6502()


def pram(*args): # mem, addr
    mem = args[0]
    addr = None if not len(args) == 2 else args[1]

    if addr is None:
        addr = cur_addr
    if mem is None:
        val = cpu.ram(addr)
        return '#%s @ %s' % (hex(val), hex(addr))
    else:
        val = cpu.ram(addr)
        cpu.ram(addr, mem)
        return '#%s -> %s (%s)' % (hexf(mem), hexf(addr, 4), hexf(val))


def dumpram(*args): # stop
    global cur_addr
    out = ''

    if not stop:
        cur_addr += 1
        return pram(cur_addr - 1)
    for addr in range(cur_addr, cur_addr + stop):
        out += pram(addr) + '\n'

    return out


def reg(*args):
    out = ''
    registers = {'acc':cpu.acc, 'x':cpu.x, 'y':cpu.y,
            'sp':cpu.sp, 'p':cpu.p}

    if len(args) == 0:
        data = map(lambda reg: reg(), registers.values())
        matched = zip(registers, map(hexf, data)) + [('pc', hexf(cpu.pc(), 4))]
        for r in [x[0]+' '+x[1]+' ' for x in matched]:
            out += r
    elif len(args) == 1:
        if args[0] == 'pc':
            padding, register = 4, cpu.pc
        else:
            padding, register = 2, registers[args[0]]
        out = '%s %s' % (args[0], hexf(register(), padding))
    elif len(args) == 2:
        val = int(args[1], 16)
        register = cpu.pc if args[0] not in registers else registers[args[0]]
        pad = 4 if args[0] == 'pc' else 2
        old = register() 

        register(val)
        out = '#%s -> %s (%s)' % \
                (hexf(register(), pad), args[0], hexf(old, pad))

    return out


def dumpflags(*args):
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


def writebytes(*args): # mem
    bytes = []

    for arg in args:
        cur = arg
        if len(cur) % 2:
            cur = '0' + cur
        if len(cur) > 2:
            cur = [int(cur[c:c + 2], 16) for c in range(0, len(cur), 2)]
            bytes.extend(cur)
        else:
            bytes.append(int(cur, 16))
    
    output = ''

    for pos in zip(bytes, range(cur_addr, cur_addr + len(bytes))):
        byte, addr = pos[0], pos[1]
        output += pram(byte, addr) + '\n'
    else:
        output = output.strip()

    jumpto(cur_addr + len(bytes))

    return output


def _help(*args):
    return ', '.join(sorted([w for w in cmds]))


#
# parsing, ui

cmdpkg = namedtuple('cmdpkg', 'func args mina maxa')

cmds = {                            # 'exit' not included (handled in main)
        'step':     {'func':step,       'mina':0, 'maxa':0},
        'reset':    {'func':reset,      'mina':0, 'maxa':0},
        'cc':       {'func':jumpto,     'mina':0, 'maxa':1},
        'pram':     {'func':pram,       'mina':0, 'maxa':-1},
        'dmp':      {'func':dumpram,    'mina':0, 'maxa':2},
        'reg':      {'func':reg,        'mina':0, 'maxa':2},
        'flg':      {'func':dumpflags,  'mina':0, 'maxa':0},
        'wri':      {'func':writebytes, 'mina':1, 'maxa':-1},
        'help':     {'func':_help,      'mina':0, 'maxa':-1},
        }


def parse(str_in):
    str_in = str_in.split()
    pre = cmds[str_in[0]] if str_in[0] in cmds.keys() else cmds['wri']

    if len(str_in) == 1 and pre['func'] is not writebytes:
        args = ()
    elif pre['func'] is writebytes:
        args = tuple(str_in) if str_in[0] != 'wri' else tuple(str_in[1:])
    else:
        args = tuple(str_in[1:])

    func, mina, maxa = pre['func'], pre['mina'], pre['maxa']

    if not (mina <= len(args) <= maxa) and maxa != -1:
        raise TypeError

    return cmdpkg(func=func, args=args, mina=mina, maxa=maxa)


if __name__ == '__main__':
    print('hello')

    while True:
        prompt_text = hexf(cur_addr, 4)
        str_in = raw_input(prompt_text + '> ')

        if 'exit' in str_in:
            break
        elif not len(str_in):
            cmd = None
        else: 
            try:
                cmd = parse(str_in)
            except:
                print('error parsing \'%s\'' % str_in)
                cmd = None

        #try:
        output = cmd.func(*cmd.args) if cmd is not None else None
        #except BaseException as error:
        #    output = 'error: %s' % error

        if output is not None and len(output):
            for line in output.split('\n'):
                print(' %s' % line)

    print('goodbye')

