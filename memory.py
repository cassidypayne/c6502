#
# data storage.

class Register:
    def __init__(self, size, val=0x0):
        self._size = size
        self._val = val

    def __call__(self, val=None):
        if val is None:
            return self._val
        else:
            if self._size == 1:
                self._val = val % 0x100
            elif self._size == 2:
                self._val = val % 0x10000


class Flag:
    def __init__(self, val=False):
        self._val = bool(val)

    def __call__(self, val=None):
        if val is None:
            return self._val
        else:
            self._val = bool(val)


class Memory:
    def __init__(self):
        self._ram = [0] * 0x10000

    def __call__(self, addr, val=None):
        if val is None:
            return self._ram[addr % 0x10000]
        else:
            self._ram[addr % 0x10000] = val % 0x100
