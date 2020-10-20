# This work is licensed under the
# Creative Commons Attribution 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/
# or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

import _io
from typing import *
import re

class token():
    def __init__(self, tokenType: str, tokenValue: str, line: int, position: int) -> None:
        """
        :param tokenType: String that defines the type of token
        :param tokenValue: String, the value of the token
        :param line: Int, the line the token is on
        :param position: Int, the position on the line the token starts at
        """
        self.type = tokenType
        self.value = tokenValue
        self.line = line
        self.position = position

    def __str__(self):
        return f"token(type='{self.type}', value='{self.value}', line={self.line}, pos={self.position})"

types = {
    "int": "^\d+?$",
    "float": "^\d+?\.\d+?$",
    "str": "^((\".*?\")|(\'.*?\'))$"
}

def tokenize(file, strings=False) -> List[Union[token, str]]:
    """
    :param file: A file from open() must be in read mode
    :param strings: A bool, will return strings if this is true
    :return: a list of tokens
    """
    tokens = []
    lines = file.readlines()
    lastx = 0
    y = 0
    for x in range(len(lines)):
        line = lines[x]
        print(line)
        bits = []
        bit = ""
        max = len(line)
        y = 0
        while y < max:
            if line[y] != " ":
                bit += line[y]
                print(line[y])
                if bit.startswith("\""):
                    y+=1
                    while line[y] != "\"":
                        bit += line[y]
                        y+=1
                    y+=1
                    bits.append(bit+"\"")
                    bit = ""
                elif bit.startswith("\'"):
                    y+=1
                    while line[y] != "\'":
                        bit += line[y]
                        y+=1
                    y+=1
                    bits.append(bit+"\'")
                    bit = ""
            else:
                bits.append(bit)
                bit = ""
            y+=1

        for i in bits:
            tokens.append(
                token(
                    getType(i),
                    i,
                    x,
                    y
                )
            )

        lastx = x

        tokens.append(token("eol", "", x, y+1))
    tokens.append(token("eof", "", lastx, y+2))

    if strings:
        tokens = [str(i) for i in tokens]

    return tokens

def getType(bit: str) -> str:
    for x, y in zip(types.keys(), types.values()):
        if re.match(y, bit):
            return x

    return "param"

print(tokenize(open("test.bsm", "r"), True))
