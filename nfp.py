#!/bin/env python3

# Nufipi - Numerical File Picker

import os
import pathlib
import subprocess
import sys


class InvalidInput(Exception):
    def __init__(self):
        super().__init__("Invalid input.")


class Parser:
    def __init__(self):
        self.st = self.get_status()

    def execute(self, subcmd, ops):
        idx = self.parse_input(ops)
        files = self.parse_status(idx)
        cmd = self.get_cmd() + subcmd + files
        subprocess.run(cmd)

    def get_cmd(self) -> list:
        raise NotImplementedError

    def get_status(self):
        raise NotImplementedError

    def print_status(self):
        width = len(str(len(self.st)-1))
        for i, f in enumerate(self.st):
            print("{i:{w}d}:".format(i=i, w=width), f)

    def parse_input(self, input_string):
        if not input_string.replace(" ", "").replace("-", "").isnumeric():
            raise InvalidInput
        idx = set()
        for t in input_string.split():
            if "-" in t:
                tt = t.split("-")
                if len(tt) != 2 or not tt[0] or not tt[1]:
                    raise InvalidInput
                a, b = int(tt[0]), int(tt[1])
                a, b = (a, b) if a < b else (b, a)
                idx.update(range(a, b+1))
            else:
                idx.add(int(t))
        # return sorted(list(idx))
        return idx

    def parse_status(self, idx):
        if max(idx) > len(self.st) - 1:
            raise InvalidInput
        files = [self.parse_status_line(self.st[i]) for i in idx]
        return files

    def parse_status_line(self, line):
        raise NotImplementedError


class GitParser(Parser):
    def get_status(self):
        """git status"""
        p = subprocess.run(["git", "status", "--porcelain", "--no-renames"], capture_output=True, text=True)
        res = [l for l in p.stdout.split("\n") if l]
        return res

    def parse_status_line(self, line):
        line = line[3:]
        return line[1:-1] if line.startswith('"') and line.endswith('"') else line

    def get_cmd(self):
        return ["git"]


class LsParser(Parser):
    def get_status(self):
        p = pathlib.Path()
        return list(p.iterdir())

    def parse_status_line(self, line):
        return line

    def get_cmd(self):
        return []


def get_parser():
    parser_type = LsParser # default parser
    argc = len(sys.argv)
    if argc == 1:
        args = []
    elif sys.argv[1] == "--parser":
        if argc < 3:
            exit("Parser not specified.")
        chosen_parser = sys.argv[2]
        if chosen_parser == "ls":
            parser_type = LsParser
        elif chosen_parser == "git":
            parser_type = GitParser
        else:
            exit("Invalid parser.")
        args = sys.argv[3:]
    else:
        args = sys.argv[1:]
    return parser_type(), args


if __name__ == "__main__":
    parser, args = get_parser()
    if args:
        print("Select files:")
        parser.print_status()
        ops = input("Enter: ")
        parser.execute(args, ops)
    else:
        parser.print_status()
