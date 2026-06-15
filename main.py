import sys, math


def main(name):
    print(f"Hello from {name}")


def process_a_ins(cmd):
    num = cmd.lstrip("@")
    return num


def is_a_ins(cmd):
    if cmd.startswith("@"):
        return True


def num_to_16_bit_binary(num):
    res = ""
    while num >= 1:
        res = str(num % 2) + res
        num = math.floor(num / 2)

    res = "0" * (16 - len(res)) + res

    return res


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

    # A-instruction
    #    for line in clean_list:
    #        if is_a_ins(line):
    #            num = int(line.lstrip("@"))
    #            binary = num_to_16_bit_binary(num)
    #            with open(f"{filename.rstrip('.asm')}.hack", "w+") as f:
    #                f.write(binary)
    print(clean_list)
