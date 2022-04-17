from sys import argv
from parser import parse_model


def main() -> None:
    if len(argv) < 2:
        raise Exception("No file provided")

    model = parse_model(argv[1])
    model.solve()
    model.print_optimal()


if __name__ == "__main__":
    main()
