import json
import os
import re
from argparse import ArgumentParser, ArgumentTypeError

from uvm import UVM


def main():
    argParser = ArgumentParser()
    argParser.add_argument("-x", "--executable", required=True, help="path to the binary file with the assembled program")
    argParser.add_argument("-d", "--dump", required=True, help="path to the file where the memory dump will be saved after the program is executed")
    argParser.add_argument("-dr", "--dump-range", required=True, type=regex_type("^(0x[a-fA-F0-9]+|[0-9]+)-(0x[a-fA-F0-9]+|[0-9]+)$"),
                           help="range of memory addresses for dump output (example: -dr 1024-2048)")
    argParser.add_argument("-t", "--test", action="store_true", default=False, help="fill mem 80-84 with random values")

    args = argParser.parse_args()

    uvm = None
    try:
        code = load_code(args.executable)
        print(f"running {args.executable}")
        uvm = UVM(code)
        if args.test:
            uvm.init_test()
        uvm.start()
        dump = uvm.dump_mem(*(int(v, 16) if v.startswith("0x") else int(v) for v in args.dump_range.split("-")))
        uvm = None
        save_dump(args.dump, dump)
        print(f"dump memory to {args.dump}")
    except Exception as x:
        print(x)
        if uvm:
            try:
                dump = uvm.dump_mem(*(int(v, 16) if v.startswith("0x") else int(v) for v in args.dump_range.split("-")))
                save_dump(args.dump, dump)
                print(f"dump memory to {args.dump}")
            except Exception:
                print(f"pc={uvm.regs.pc}")


def load_code(fname: str):
    with open(fname, "rb") as f:
        return f.read()


def save_dump(fname: str, data):
    dirn = os.path.dirname(fname)
    if dirn and not os.path.exists(dirn):
        os.makedirs(dirn)
    with open(fname, "w", encoding="utf8") as f:
        json.dump(data, f, indent=4)


def regex_type(pattern: str):
    def closure_check_regex(arg_value):
        if not re.match(pattern, arg_value):
            raise ArgumentTypeError(f"invalid value: not {pattern}")
        return arg_value
    return closure_check_regex


if __name__ == "__main__":
    main()
