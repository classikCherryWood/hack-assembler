import sys


def main(name):
    print(f"Hello from {name}")


class HackAssembler:
    pass


if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename, "r") as f:
        code_list = f.readlines()

    clean_list: list[str] = []
    for line in code_list:
        # remove leading spaces & trailing \n char
        clean_line = line.lstrip().rstrip()
        # remove empty char & comments
        if clean_line and not clean_line.startswith("//"):
            clean_list.append(clean_line)

    print(clean_list)
