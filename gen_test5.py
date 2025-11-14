from argparse import ArgumentParser
from random import randint

import yaml


def main():
    argParser = ArgumentParser()
    argParser.add_argument("-o", "--output", required=True)
    args = argParser.parse_args()

    # code = []
    # # gen_vector(code, 160, [2, 3, 4, 5, 6])
    # # gen_vector(code, 176, [2, 2, 4, 4, 6])
    # gen_vector(code, 160)
    # gen_vector(code, 176)
    # gen_compare(code, 160, 176)

    # with open(args.output, "w", encoding="utf8") as f:
    #     yaml.dump(code, f, default_flow_style=False, allow_unicode=True)
    with open(args.output, "w", encoding="utf8") as f:
        code = []
        vec = gen_vector(code, 160)
        f.write(f"# write vector {vec} to adress 160\n")
        f.write(yaml.dump(code))
        code = []
        vec = gen_vector(code, 176, [11 - v if randint(0, 1) == 1 else v for v in vec])
        f.write(f"# write vector {vec} to adress 176\n")
        f.write(yaml.dump(code))
        code = []
        gen_compare(code, 160, 176)
        f.write("# compare vectors\n")
        f.write(yaml.dump(code))


def gen_vector(code: list, si: int, vec: list | None = None):
    if not vec:
        vec = [randint(2, 10) for i in range(5)]
    for i, v in enumerate(vec):
        code.append({
            "op": "load_const",
            "value": v,
            "dest_addr": 1,
        })
        code.append({
            "op": "load_const",
            "value": si + i,
            "dest_addr": 2,
        })
        code.append({
            "op": "write_mem",
            "src_reg_addr": 1,
            "dest_mem_reg_addr": 2,
        })
    return vec


def gen_compare(code: list, si1: int, si2: int):
    code.append({
        "op": "load_const",
        "value": si1,
        "dest_addr": 2,
    })
    for i in range(5):
        code.append({
            "op": "read_mem",
            "dest_addr": 1,
            "src_addr": si2 + i,
        })
        code.append({
            "op": "bin_eq",
            "left_mem_addr": si1 + i,
            "right_reg_addr": 1,
            "result_base_reg_addr": 2,
            "offset": i,
        })


if __name__ == "__main__":
    main()
