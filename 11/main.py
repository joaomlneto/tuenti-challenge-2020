#!/usr/bin/env python3

import argparse
import icu
import os
import re
import sys

parser = argparse.ArgumentParser(description="Tuenti Challenge 2020 - Problem 07")
parser.add_argument("-f", "--file", dest="filename", type=str,
                    help="the text file to analyze", required=True)
args = parser.parse_args()

stack = [] # debug - print sums

def get_list_as_string(lst):
    return '(' + ','.join(str(x) for x in sorted(lst)) + ')'

# implemented cache for the final submission challenge! was too slow!
cache = dict()

def count_sums(n, available):
    if n == 0: return 1
    if n < 0:  return 0
    if n in cache and get_list_as_string(available) in cache[n]:
        return cache[n][get_list_as_string(available)]

    total = 0
    for i in range(0, len(available)):
        #stack.append(available[i])
        total += count_sums(n - available[i], available[i:])
        #stack.pop()

    if n not in cache: cache[n] = dict()
    cache[n][get_list_as_string(available)] = total

    #print('number of ways of adding to %d = %d' % (n, total))
    return total

# compute how often each word appears
with open(args.filename, 'r') as file:
    num_cases = int(next(file))
    for i in range(0, num_cases):
        n, *excluded = [int(x) for x in str(next(file)).split()]
        #print(n, excluded)
        all = list(range(1, n))
        available = list(set(all) - set(excluded))
        #print('available', available)
        cached = {}
        print('Case #%d: %d' % (i + 1, count_sums(n, available)))
        #print(cached, '\n\n')
