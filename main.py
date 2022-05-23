from sys import argv
from parser import parse_model
from solvers import simplex_solver


def main() -> None:
    if len(argv) < 2:
        raise Exception("No file provided")

    model = parse_model(argv[1])
    simplex_solver(model)


if __name__ == "__main__":
    main()
