from instructionset import *

_sizes = {  # mode: size (in bytes).
    'acc': 1,
    'abs': 3,
    'abx': 3,
    'aby': 3,
    'imm': 2,
    'imp': 1,
    'ind': 2,
    'iix': 2,
    'iiy': 2,
    'rel': 2,
    'zpg': 2,
    'zpx': 2,
    'zpy': 2
}

#
# main index.

_instructions = {  # instruction byte: func, mode.
    0x69: (ADC, 'imm'),  # ADC
    0x65: (ADC, 'zpg'),
    0x75: (ADC, 'zpx'),
    0x6d: (ADC, 'abs'),
    0x7d: (ADC, 'abx'),
    0x79: (ADC, 'aby'),
    0x61: (ADC, 'iix'),
    0x71: (ADC, 'iiy'),
    0x29: (AND, 'imm'),  # AND
    0x25: (AND, 'zpg'),
    0x35: (AND, 'zpx'),
    0x2d: (AND, 'abs'),
    0x3d: (AND, 'abx'),
    0x39: (AND, 'aby'),
    0x21: (AND, 'iix'),
    0x31: (AND, 'iiy'),
    0x0a: (ASL, 'acc'),  # ASL
    0x06: (ASL, 'zpg'),
    0x16: (ASL, 'zpx'),
    0x0e: (ASL, 'abs'),
    0x1e: (ASL, 'abx'),
    0x90: (BCC, 'rel'),  # BCC
    0xb0: (BCS, 'rel'),  # BCS
    0xf0: (BEQ, 'rel'),  # BEQ
    0x24: (BIT, 'zpg'),  # BIT
    0x2c: (BIT, 'abs'),
    0x30: (BMI, 'rel'),  # BMI
    0xd0: (BNE, 'rel'),  # BNE
    0x10: (BPL, 'rel'),  # BPL
    0x00: (BRK, 'imp'),  # BRK
    0x50: (BVC, 'rel'),  # BVC
    0x18: (CLC, 'imp'),  # CLC
    0xd8: (CLD, 'imp'),  # CLD
    0x58: (CLI, 'imp'),  # CLI
    0xb8: (CLV, 'imp'),  # CLV
    0xc9: (CMP, 'imm'),  # CMP
    0xc5: (CMP, 'zpg'),
    0xd5: (CMP, 'zpx'),
    0xcd: (CMP, 'abs'),
    0xdd: (CMP, 'abx'),
    0xd9: (CMP, 'aby'),
    0xc1: (CMP, 'iix'),
    0xd1: (CMP, 'iiy'),
    0xe0: (CPX, 'imm'),  # CPX
    0xe4: (CPX, 'zpg'),
    0xec: (CPX, 'abs'),
    0xc0: (CPY, 'imm'),  # CPY
    0xc4: (CPY, 'zpg'),
    0xcc: (CPY, 'abs'),
    0xc6: (DEC, 'zpg'),  # DEC
    0xd6: (DEC, 'zpx'),
    0xce: (DEC, 'abs'),
    0xde: (DEC, 'abx'),
    0xca: (DEX, 'imp'),  # DEX
    0x88: (DEY, 'imp'),  # DEY
    0x49: (EOR, 'imm'),  # EOR
    0x45: (EOR, 'zpg'),
    0x55: (EOR, 'zpx'),
    0x4d: (EOR, 'abs'),
    0x5d: (EOR, 'abx'),
    0x59: (EOR, 'aby'),
    0x41: (EOR, 'iix'),
    0x51: (EOR, 'iiy'),
    0xe6: (INC, 'zpg'),  # INC
    0xf6: (INC, 'zpx'),
    0xee: (INC, 'abs'),
    0xfe: (INC, 'abx'),
    0xe8: (INX, 'imp'),  # INX
    0xc8: (INY, 'imp'),  # INY
    0x4c: (JMP, 'abs'),  # JMP
    0x6c: (JMP, 'ind'),
    0x20: (JSR, 'abs'),  # JSR
    0xa9: (LDA, 'imm'),  # LDA
    0xa5: (LDA, 'zpg'),
    0xb5: (LDA, 'zpx'),
    0xad: (LDA, 'abs'),
    0xbd: (LDA, 'abx'),
    0xb9: (LDA, 'aby'),
    0xa1: (LDA, 'iix'),
    0xb1: (LDA, 'iiy'),
    0xa2: (LDX, 'imm'),  # LDX
    0xa6: (LDX, 'zpg'),
    0xb6: (LDX, 'zpy'),
    0xae: (LDX, 'abs'),
    0xbe: (LDX, 'aby'),
    0xa0: (LDY, 'imm'),  # LDY
    0xa4: (LDY, 'zpg'),
    0xb4: (LDY, 'zpx'),
    0xac: (LDY, 'abs'),
    0xbc: (LDY, 'abx'),
    0x4a: (LSR, 'acc'),  # LSR
    0x46: (LSR, 'zpg'),
    0x56: (LSR, 'zpx'),
    0x4e: (LSR, 'abs'),
    0x5e: (LSR, 'abx'),
    0xea: (NOP, 'imp'),  # NOP
    0x09: (ORA, 'imm'),  # ORA
    0x05: (ORA, 'zpg'),
    0x15: (ORA, 'zpx'),
    0x0d: (ORA, 'abs'),
    0x1d: (ORA, 'abx'),
    0x19: (ORA, 'aby'),
    0x01: (ORA, 'iix'),
    0x11: (ORA, 'iiy'),
    0x48: (PHA, 'imp'),  # PHA
    0x28: (PHP, 'imp'),  # PHP
    0x68: (PLA, 'imp'),  # PLA
    0x2a: (ROL, 'acc'),  # ROL
    0x26: (ROL, 'zpg'),
    0x36: (ROL, 'zpx'),
    0x2e: (ROL, 'abs'),
    0x3e: (ROL, 'abx'),
    0x6a: (ROR, 'acc'),  # ROR
    0x66: (ROR, 'zpg'),
    0x76: (ROR, 'zpx'),
    0x6e: (ROR, 'abs'),
    0x7e: (ROR, 'abx'),
    0x40: (RTI, 'imp'),  # RTI
    0x60: (RTS, 'imp'),  # RTS
    0xe9: (SBC, 'imm'),  # SBC
    0xe5: (SBC, 'zpg'),
    0xf5: (SBC, 'zpx'),
    0xed: (SBC, 'abs'),
    0xfd: (SBC, 'abx'),
    0xf9: (SBC, 'aby'),
    0xe1: (SBC, 'iix'),
    0xf1: (SBC, 'iiy'),
    0x38: (SEC, 'imp'),  # SEC
    0xf8: (SED, 'imp'),  # SED
    0x78: (SEI, 'imp'),  # SEI
    0x85: (STA, 'zpg'),  # STA
    0x95: (STA, 'zpx'),
    0x8d: (STA, 'abs'),
    0x9d: (STA, 'abx'),
    0x99: (STA, 'aby'),
    0x81: (STA, 'iix'),
    0x91: (STA, 'iiy'),
    0x86: (STX, 'zpg'),  # STX
    0x96: (STX, 'zpy'),
    0x8e: (STX, 'abs'),
    0x84: (STY, 'zpg'),  # STY
    0x94: (STY, 'zpx'),
    0x8c: (STY, 'abs'),
    0xaa: (TAX, 'imp'),  # TAX
    0xa8: (TAY, 'imp'),  # TAY
    0xba: (TSX, 'imp'),  # TSZ
    0x8a: (TXA, 'imp'),  # TXA
    0x9a: (TXS, 'imp'),  # TXS
    0x98: (TYA, 'imp'),  # TYA
}


def get_instruction(opcode):
    return _instructions[opcode][0]


def get_mode(opcode):
    return _instructions[opcode][1]


def get_size(opcode):
    return _sizes[_instructions[opcode][1]]
