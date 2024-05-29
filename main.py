
from parsing import parse_pls
from filter import filter_pls
from pnd import save_pls


def main():
    parse_pls()
    filter_pls()
    save_pls()


if __name__ == "__main__":
    main()
