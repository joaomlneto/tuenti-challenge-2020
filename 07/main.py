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

mapping = {
    "'": 'q',
    ',': 'w',
    '.': 'e',
    'p': 'r',
    'y': 't',
    'f': 'y',
    'g': 'u',
    'c': 'i',
    'r': 'o',
    'l': 'p',
    '?': '[UNKNOWN]',
    '+': '[UNKNOWN]',

    'a': 'a',
    'o': 's',
    'e': 'd',
    'u': 'f',
    'i': 'g',
    'd': 'h',
    'h': 'j',
    't': 'k',
    'n': 'l',
    's': ';',

    ';': 'z',
    'q': 'x',
    'j': 'c',
    'k': 'v',
    'x': 'b',
    'b': 'n',
    'm': 'm',
    'w': ',',
    'v': '.',
    'z': '/',

    ' ': ' ',
    '\n': '\n',
    
    '0': '0',
    '1': '1',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',

    '(': '(',
    ')': ')',

    '-': "'"
}

# compute how often each word appears
with open(args.filename, 'r') as file:
    num_cases = int(next(file))
    for i in range(0, num_cases):
        encrypted_line = str(next(file))
        out = ''.join([mapping[x.lower()] if x in mapping else '[?????]' for x in encrypted_line]).rstrip().ljust(80, ' ')
        print('Case #%i: %s\n' % (i + 1, out), end='')

