from random import randint
from operations import Operation

MEMSIZE = 64 * 1024 * 1024  # 64mb


class UVM:
    memory: bytearray
    regs: "Registers"

    def __init__(self, code: bytes):
        self.regs = Registers()
        self.memory = bytearray(MEMSIZE)
        self.memory[0:len(code)] = code

    def start(self):
        while True:
            fb = self.memory[self.regs.pc]
            if not fb:
                break
            op = Operation.decode(fb, self)
            op.execute(self)

    def get_word(self, word_len: int):
        word = self.memory[self.regs.pc:self.regs.pc + word_len]
        self.regs.pc += word_len
        return word

    def dump_mem(self, s: int, e: int):
        memory = {}
        S = 16
        s = s // S * S
        for i in range(s, e + 1, S):
            memory[f"{i:06X}"] = self.memory[i:min(i + S, e + 1)].hex(" ").upper()
        return {"regs": self.regs.dump(), "memory": memory}

    def init_test(self):
        for i in range(80, 85):
            self.memory[i] = randint(0, 255)


class Registers:
    _regs: dict[int, int]

    @property
    def pc(self):
        return self._regs[0]

    @pc.setter
    def pc(self, v: int):
        self._regs[0] = v % MEMSIZE

    def __init__(self) -> None:
        self._regs = {i: 0 for i in range(16)}

    def __getitem__(self, key: int):
        return self._regs[key] if key in self._regs else 0

    def __setitem__(self, key: int, v: int):
        self._regs[key] = v

    def dump(self):
        return {("PC" if k == 0 else f"{k:X}"): v for k, v in self._regs.items()}
