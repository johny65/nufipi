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
        raise Exception("Invalid input.")
    idx = set()
    for t in input_string.split():
        if "-" in t:
            tt = t.split("-")
            if len(tt) != 2 or not tt[0] or not tt[1]:
                raise Exception("Invalid input.")
            a, b = int(tt[0]), int(tt[1])
            a, b = (a, b) if a < b else (b, a)
            idx.update(range(a, b+1))
        else:
            idx.add(int(t))
    # return sorted(list(idx))
    return idx

def parse_status(st, idx):
    if max(idx) > len(st) - 1:
        raise Exception("Invalid input.")
    files = [parse_status_line(st[i]) for i in idx]
    return files

def parse_status_line(line):
    line = line[3:]
    return line[1:-1] if line.startswith('"') and line.endswith('"') else line


if __name__ == "__main__":
    st = get_status()
    if len(sys.argv) == 1:
        print_status(st)
    else:
        print("Select files:")
        print_status(st)
        ops = input("Enter: ")
        ops = parse_input(ops)

        files = parse_status(st, ops)
        cmd = ["git"] + sys.argv[1:] + files
        # cmd = "git {} -- {}".format(" ".join(sys.argv[1:]), " ".join(files))

        subprocess.run(cmd)
    # print(os.getcwd())
