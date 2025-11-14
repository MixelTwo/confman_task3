from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from uvm import UVM


class Operation:
    __operations: dict[str, type["Operation"]] = {}
    __operationsi: dict[int, type["Operation"]] = {}
    op: int
    name: str
    args: dict[str, int]

    def __init__(self):
        self.args = {}

    @staticmethod
    def create(data: Any):
        if not isinstance(data, dict):
            raise Exception("not command")
        if "op" not in data:
            raise Exception("has not 'op' field")
        name = data["op"]
        if name not in Operation.__operations:
            raise Exception(f"unknown operation '{name}'")
        opr = Operation.__operations[name]()
        args = opr._args()
        for k, v in data.items():
            if k == "op":
                continue
            if k not in args:
                raise Exception(f"'{k}' field is unknown for {name} operation")
            args.pop(args.index(k))
            if not isinstance(v, int):
                raise Exception(f"'{k}' field not int")
            opr.args[k] = v
            setattr(opr, k, v)
        if len(args) > 0:
            raise Exception(f"{", ".join(map(repr, args))} field{"s" if len(args) > 1 else ""} are missing in {name} operation")
        return opr

    @staticmethod
    def decode(fb: int, uvm: "UVM"):
        op = fb & 0b111111
        if op not in Operation.__operationsi:
            raise Exception(f"unknown operation '{op}'")
        return Operation.__operationsi[op]().from_bytes(uvm)

    def __init_subclass__(cls) -> None:
        Operation.__operations[cls.name] = cls
        Operation.__operationsi[cls.op] = cls

    def __repr__(self) -> str:
        return f"Operation(name={repr(self.name)}, args={self.args})"

    def _args(self):
        return [v[0] for v in self.__annotations__.items() if v[1] and v[0] != "op"]

    def to_bytes(self) -> bytes:
        raise NotImplementedError("Not Implemented")

    def from_bytes(self, uvm: "UVM") -> "Operation":
        raise NotImplementedError("Not Implemented")

    def execute(self, uvm: "UVM"):
        raise NotImplementedError("Not Implemented")


class _(Operation):
    name = "load_const"
    op = 43
    value: int
    dest_addr: int

    def to_bytes(self) -> bytes:
        word = 0
        word |= (self.op & 0b111111)          # A bits 0-5
        word |= (self.value & 0xFFF) << 6     # B bits 6-17 (12 bits)
        word |= (self.dest_addr & 0xF) << 18  # C bits 18-21 (4 bits)
        return word.to_bytes(3, "little")

    def from_bytes(self, uvm: "UVM"):
        word = uvm.get_word(3)
        w = int.from_bytes(word, "little")
        self.value = (w >> 6) & 0xFFF      # 12 bits (B)
        self.dest_addr = (w >> 18) & 0xF   # 4 bits (C)
        return self

    def execute(self, uvm: "UVM"):
        uvm.regs[self.dest_addr] = self.value


class _(Operation):
    name = "read_mem"
    op = 60
    dest_addr: int
    src_addr: int

    def to_bytes(self) -> bytes:
        word = 0
        word |= self.op & 0b111111                 # A bits 0–5
        word |= (self.dest_addr & 0xF) << 6        # B bits 6–9 (4 bits)
        word |= (self.src_addr & 0x3FFFFFF) << 10  # C bits 10–35 (26 bits)
        return word.to_bytes(5, "little")

    def from_bytes(self, uvm: "UVM"):
        word = uvm.get_word(5)
        w = int.from_bytes(word, "little")
        self.dest_addr = (w >> 6) & 0xF        # 4 bits (B)
        self.src_addr = (w >> 10) & 0x3FFFFFF  # 26 bits (C)
        return self

    def execute(self, uvm: "UVM"):
        uvm.regs[self.dest_addr] = uvm.memory[self.src_addr]


class _(Operation):
    name = "write_mem"
    op = 19
    src_reg_addr: int
    dest_mem_reg_addr: int

    def to_bytes(self) -> bytes:
        word = 0
        word |= self.op & 0b111111                    # A bits 0–5
        word |= (self.src_reg_addr & 0xF) << 6        # B bits 6–9 (4 bits)
        word |= (self.dest_mem_reg_addr & 0xF) << 10  # C bits 10–13 (4 bits)
        return word.to_bytes(2, "little")

    def from_bytes(self, uvm: "UVM"):
        word = uvm.get_word(2)
        w = int.from_bytes(word, "little")
        self.src_reg_addr = (w >> 6) & 0xF        # 4 bits (B)
        self.dest_mem_reg_addr = (w >> 10) & 0xF  # 4 bits (C)
        return self

    def execute(self, uvm: "UVM"):
        uvm.memory[uvm.regs[self.dest_mem_reg_addr]] = uvm.regs[self.src_reg_addr] & 0xFF


class _(Operation):
    name = "bin_eq"
    op = 25
    result_base_reg_addr: int
    left_mem_addr: int
    right_reg_addr: int
    offset: int

    def to_bytes(self) -> bytes:
        word = 0
        word |= self.op & 0b111111                      # A bits 0–5
        word |= (self.result_base_reg_addr & 0xF) << 6  # B bits 6–9 (4 bits)
        word |= (self.left_mem_addr & 0x3FFFFFF) << 10  # C bits 10–35 (26 bits)
        word |= (self.right_reg_addr & 0xF) << 36       # D bits 36–39 (4 bits)
        word |= (self.offset & 0x7F) << 40              # E bits 40–46 (7 bits)
        return word.to_bytes(6, "little")

    def from_bytes(self, uvm: "UVM"):
        word = uvm.get_word(6)
        w = int.from_bytes(word, "little")
        self.result_base_reg_addr = (w >> 6) & 0xF  # 4 bits (B)
        self.left_mem_addr = (w >> 10) & 0x3FFFFFF  # 26 bits (C)
        self.right_reg_addr = (w >> 36) & 0xF       # 4 bits (D)
        self.offset = (w >> 40) & 0x7F              # 7 bits (E)
        return self

    def execute(self, uvm: "UVM"):
        pass
