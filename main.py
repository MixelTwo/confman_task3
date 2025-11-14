import os
from argparse import ArgumentParser

import yaml

from operations import Operation


def main():
    argParser = ArgumentParser()
    argParser.add_argument("-s", "--source", required=True, help="the path to the source file with the program text")
    argParser.add_argument("-o", "--output", required=True, help="the path to the binary result file")
    argParser.add_argument("-t", "--test", action="store_true", default=False, help="testing mode")

    args = argParser.parse_args()

    try:
        source = load_source(args.source)
        print(f"loaded from {args.source}")
        result = [opr.to_bytes() for opr in source]

        if args.test:
            print("\n".join(f"{i}: {v.hex(" ")}" for i, v in enumerate(result)))
        print(f"{len(result)} commands assembled")

        save_output(args.output, result)
        print(f"output to {args.output}")
    except Exception as x:
        print(x)
        return


def load_source(fname: str):
    with open(fname, encoding="utf8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, list):
        raise Exception("source wrong format: not list of commands")

    operations: list[Operation] = []
    errors: list[str] = []
    for i, el in enumerate(data):
        try:
            operations.append(Operation.create(el))
        except Exception as x:
            errors.append(f"item #{i}: {x}")
    if errors:
        raise Exception("source wrong format:\n\t" + "\n\t".join(errors))

    return operations


def save_output(fname: str, data: list[bytes]):
    dirn = os.path.dirname(fname)
    if dirn and not os.path.exists(dirn):
        os.makedirs(dirn)
    with open(fname, "wb") as f:
        for b in data:
            f.write(b)


if __name__ == "__main__":
    main()
