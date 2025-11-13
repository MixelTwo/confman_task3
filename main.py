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
    except Exception as x:
        print(x)
        return

    print("\n".join(map(str, source)))


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


if __name__ == "__main__":
    main()
