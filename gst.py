#!/bin/env python3

import os
import subprocess
import sys

def get_status():
    """git status"""
    p = subprocess.run(["git", "status", "--porcelain", "--no-renames"], capture_output=True, text=True)
    res = [l for l in p.stdout.split("\n") if l]
    return res

def print_status(st):
    width = len(str(len(st)-1))
    for i, f in enumerate(st):
        print("{i:{w}d}:".format(i=i, w=width), f)

def parse_input(input_string):
    if not input_string.replace(" ", "").replace("-", "").isnumeric():
        raise Exception("Cadena inválida.")
    idx = []
    for t in input_string.split():
        if "-" in t:
            tt = t.split("-")
            if len(tt) != 2 or not tt[0] or not tt[1]:
                raise Exception("Cadena inválida.")
            idx.append(tt[0])
            idx.append(tt[1])
        else:
            idx.append(t)
    return idx

if __name__ == "__main__":
    st = get_status()
    if len(sys.argv) == 1:
        print_status(st)
    else:
        print("Seleccione los archivos:")
        print_status(st)
        ops = input("Ingrese:")

        print(parse_input(ops))
    # print(os.getcwd())
