import sys, math
from symboltable import SymbolTable

class Parser:
    def __init__(self, filename):
        raw = self._read(filename)
        trimmed = self._trim(raw)
        self.lines = self._remove_comment(trimmed)

    def _read(self, filename):
        with open(filename, "r") as f:
            return f.readlines()

    def _trim(self, raw):
        """
        removing leading spaces & trailing \n char,
        """
        return [line.strip() for line in raw]

    def _remove_comment(self, trimmed):
        """
        removing comments starting with '//'
        """
        res = []
        for l in trimmed:
            if l and not l.startswith("//"):
                res.append(l)
        return res

    def instruction_type(self, line):
        """identify the instruction type"""
        if line.startswith("@"):
            return "A"
        if line.startswith("("):
            return "L"
        else:
            return "C"

    def symbol(self, line):
        if line.startswith("@"):
            return line[1:]
        else:
            return line[1:-1]

    def dest(self, line):
        """returns LHS from C-instruction"""
        try:
            i = line.index("=")
        except ValueError:
            return None
        return line[: line.index("=")]

    def comp(self, line):
        """returns from = to ; from C-instruction"""
        try:
            i = line.index("=")
        except ValueError:
            i = None

        try:
            j = line.index(";")
        except ValueError:
            j = None

        if i and j:
            return line[i + 1 : j]
        elif i and not j:
            return line[i + 1 :]
        elif not i and j:
            return line[:j]
        else:
            return line

    def jump(self, line):
        """returns JUMP statement if any"""
        try:
            i = line.index(";")
        except ValueError:
            return None
        return line[i + 1 :]


class Code:
    def __init__(self):
        self.dest_lookup = {"A": 0, "D": 1, "M": 2}
        self.comp_lookup = {
            "0": "0101010",
            "1": "0111111",
            "-1": "0111010",
            "D": "0001100",
            "A": "0110000",
            "M": "1110000",
            "!D": "0001101",
            "!A": "0110001",
            "!M": "1110001",
            "-D": "0001111",
            "-A": "0110111",
            "-M": "1110111",
            "D+1": "0011111",
            "1+D": "0011111",
            "A+1": "0110111",
            "1+A": "0110111",
            "M+1": "1110111",
            "1+M": "1110111",
            "D-1": "0001110",
            "A-1": "0110010",
            "M-1": "1110010",
            "D+A": "0000010",
            "A+D": "0000010",
            "D+M": "1000010",
            "M+D": "1000010",
            "D-A": "0010011",
            "D-M": "1010011",
            "A-D": "0000111",
            "M-D": "1000111",
            "D&A": "0000000",
            "A&D": "0000000",
            "D&M": "1000000",
            "M&D": "1000000",
            "D|A": "0010101",
            "A|D": "0010101",
            "D|M": "1010101",
            "M|D": "1010101",
        }
        self.jump_lookup = {
            None: "000",
            "JGT": "001",
            "JEQ": "010",
            "JGE": "011",
            "JLT": "100",
            "JNE": "101",
            "JLE": "110",
            "JMP": "111",
        }

    def bin_address(self, num: int):
        res = ""
        while num >= 1:
            res = str(num % 2) + res
            num = math.floor(num / 2)

        res = "0" * (16 - len(res)) + res
        return res

    def dest(self, dest: str):
        res = ["0", "0", "0"]
        if not dest:
            return "000"

        for d in dest:
            index = self.dest_lookup[d]
            res[index] = "1"
        return "".join(res)

    def comp(self, comp: str):
        lookup = self.comp_lookup[comp]
        return lookup

    def jump(self, jump: str):
        lookup = self.jump_lookup[jump]
        return lookup


if __name__ == "__main__":
    filename = sys.argv[1]
    parser = Parser(filename)
    code = Code()
    table = SymbolTable()
    print(parser.lines)

    # Pass 1: go through labels and record the ROM for them
    rom = 0
    for l in parser.lines: 
        t = parser.instruction_type(l)
        if t == "L":
            s = parser.symbol(l)
            table.add_entry(s, rom)
        
        else:
            rom += 1
                
    # Pass 2: go through A & C instructions , allocate for RAM, conversion 
    output = [] 
    next_ram = 16
    for l in parser.lines:
        t = parser.instruction_type(l)

        if t == "A": 
            s = parser.symbol(l)
#            print(s)
            # vanila A-instrucction
            if s.isdigit(): 
                res = code.bin_address(int(s))
                #print(res)
                output.append(res)

            else: 
                if not table.contains(s): 
                    table.add_entry(s, next_ram)
                    next_ram += 1
                addr = table.get_address(s)
                res = code.bin_address(int(addr))
                print(res)
                output.append(res)

        elif t == "C":
            d = parser.dest(l)
            c = parser.comp(l)
            j = parser.jump(l)
#            print(d, c, j)
            dd = code.dest(d)
            cc = code.comp(c)
            jj = code.jump(j)
            print("111" + cc + dd + jj)
            output.append("111" + cc + dd + jj)

    with open(filename.replace(".asm", ".hack"), 'w') as f: 
        f.write("\n".join(output))
        print("writing completed")
 


# for line in Parser.lines:
#   check instruction type (Parser)
#   if A: resolve symbol if needed with Symbol table, then convert to binary (Code)
#   if C: extract comp, dest and jump (Parser), then convert to binary (Code)
#   if labels: look up Symbol table for address, translate the corresponding address
