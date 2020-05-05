#!/usr/bin/env python3

import argparse
import icu
import os
import re
import sys

parser = argparse.ArgumentParser(description="Tuenti Challenge 2020 - Problem 05")
parser.add_argument("-f", "--file", dest="filename", type=str,
                    help="the text file to analyze", required=True)
args = parser.parse_args()

def is_tuentistic_sum_impossible(n):
  return (n < 20) or (30 <= n < 40) or (n == 59);

def tuentistic_sum(n):
  return 'IMPOSSIBLE' if is_tuentistic_sum_impossible(n) else n // 20

# compute how often each word appears
with open(args.filename, 'r') as file:
    num_cases = int(next(file))
    for i in range(0, num_cases):
        n = int(next(file))
        print('Case #%d: %s' % (i + 1, tuentistic_sum(n)))

