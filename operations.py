from typing import Any


class Operation:
    __operations: dict[str, type["Operation"]] = {}
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

    def __init_subclass__(cls) -> None:
        Operation.__operations[cls.name] = cls

    def __repr__(self) -> str:
        return f"Operation(name={repr(self.name)}, args={self.args})"

    def _args(self):
        return [v[0] for v in self.__annotations__.items() if v[1]]


class _(Operation):
    name = "load_const"
    value: int
    dest_addr: int


class _(Operation):
    name = "read_mem"
    dest_addr: int
    src_addr: int


class _(Operation):
    name = "write_mem"
    src_reg_addr: int
    dest_mem_reg_addr: int


class _(Operation):
    name = "bin_eq"
    result_base_reg_addr: int
    left_mem_addr: int
    right_reg_addr: int
    offset: int
