#!/usr/bin/env python3

import argparse
import os
import sys

parser = argparse.ArgumentParser(description="Tuenti Challenge 2020 - Problem 01")
parser.add_argument("-f", "--file", dest="filename", type=str,
                    help="file to open", required=True)
args = parser.parse_args()

with open(args.filename) as f:
    lines = list(f)
    for i, case in enumerate(lines[1:]):
        shapes = case.split()
        shapes.sort()
        if shapes[0] == 'R' and shapes[1] == 'S': # rock beats scissors
            print("Case #%d: R" % (i + 1))
        elif shapes[0] == 'P' and shapes[1] == 'S': # scissors beats paper
            print("Case #%d: S" % (i + 1))
        elif shapes[0] == 'P' and shapes[1] == 'R': # paper beats rock
            print("Case #%d: P" % (i + 1))
        else:
            print("Case #%d: -" % (i + 1))