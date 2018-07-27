#
# simple debugger / memory editor for c6502.
# python 2.7

from c6502 import C6502
from collections import namedtuple, OrderedDict

cpu = C6502()
cur_addr = 0x0

def hexf(i, w=2): # w == width in nibbles
    return '0x' + hex(i)[2:].zfill(w)


#
# commands.

def load_file(*args): # filename, addr
    pass


def jumpto(*args): # addr
    global cur_addr

    if not len(args):
        addr = cpu.pc() 
    elif type(args[0]) is str:
        addr = int(args[0], base=16) % 0x10000
    elif type(args[0]) is int:
        addr = args[0] % 0x10000

    cur_addr = addr


def step(*args):
    pcv = ['\tpc']

    if len(args):
        steps = int(args[0], 16)
    else:
        steps = 1

    for step in range(steps):
        cpu.step()
        pcv.append(hexf(cpu.pc(), 4) + '\n')

    return '\t-> '.join(pcv).strip()


def reset(*args):
    global cpu
    cpu = C6502()


def pram(*args): # addr, mem
    if not len(args):
        addr, mem = None, None
    elif len(args) == 1:
        addr, mem = args[0], None
    elif len(args) == 2:
        addr, mem = args

    addr = int(addr, 16) if type(addr) is str else addr
    mem = int(mem, 16) if type(mem) is str else mem

    if addr is None:
        addr = cur_addr

    if mem is None:
        val = cpu.ram(addr)
        return '%s -> #%s' % (hexf(addr, 4), hexf(val))
    else:
        val, mem = cpu.ram(addr), mem % 0x100
        cpu.ram(addr, mem)
        return '#%s -> %s (%s)' % (hexf(mem), hexf(addr, 4), hexf(val))


def dumpram(*args): # stop
    global cur_addr
    out = ''

    try:
        stop = int(args[0])
    except KeyError:
        stop = 0

    if not stop:
        cur_addr += 1
        return pram(cur_addr - 1)
    for addr in range(cur_addr, cur_addr + stop):
        out += pram(addr) + '\n'

    return out.strip()


def reg(*args):
    out = ''
    
    # pc is handled separately because of its width
    registers = OrderedDict([('acc', cpu.acc), ('x', cpu.x), ('y', cpu.y),
            ('sp', cpu.sp)])

    if len(args) == 0:
        data = map(lambda reg: reg(), registers.values())
        matched = zip(registers, map(hexf, data)) + [('pc', hexf(cpu.pc(), 4))]
        for r in [x[0] + ' ' + x[1] + ' ' for x in matched]:
            out += r
        else:
            out = out.strip()
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
    raw, formatted = bin(cpu.p())[2:], ''

    for letter, bit in zip('nv-bdizc', '0' * (8 - len(raw)) + raw):
        if bit == '1':
            formatted += letter.upper()
        elif bit == '0':
            formatted += letter.lower()

    return formatted + '\n' + raw.zfill(8)


def writebytes(*args): # mem
    bytes = []

    for arg in args:
        cur = arg
        if len(cur) % 2:
            cur = '0' + cur
        if len(cur) > 2:
            cur = [cur[c:c + 2] for c in range(0, len(cur), 2)]
            bytes.extend(cur)
        else:
            bytes.append(cur)

    bytes = [int(byte, 16) for byte in bytes]
    output = ''

    for pos in zip(range(cur_addr, cur_addr + len(bytes)), bytes):
        addr, byte = pos[0], pos[1]
        output += pram(hex(addr), byte) + '\n'
    else:
        output = output.strip()

    jumpto(cur_addr + len(bytes))

    return output


def _help(*args):
    return ', '.join(sorted([w for w in cmds]))


#
# parsing, ui

cmdpkg = namedtuple('cmdpkg', 'func args mina maxa')

cmds = {            # 'exit' not included (handled in __main__)
        'step':     {'func':step,       'mina':0, 'maxa':1},
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
    str_in = str_in.replace('0x', '').split()
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
        if not len(str_in) or str_in.isspace():
            cmd = None
        elif '#' in str_in.lstrip():
            cmd = None
        elif 'exit' in str_in:
            break
        else: 
            try:
                cmd = parse(str_in)
            except:
                print('error parsing \'%s\'' % str_in)
                cmd = None

        try:
            output = cmd.func(*cmd.args) if cmd is not None else None
        except BaseException as error:
            output = 'error: %s' % error

        if output is not None and len(output):
            for line in output.split('\n'):
                print(' %s' % line)

    print('goodbye')

