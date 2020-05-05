#!/usr/bin/env python3

import argparse
import gmpy2
from gmpy2 import mpz
import icu
import os
import re
import sys

byte_order = 'little' # 'little' / 'big'

parser = argparse.ArgumentParser(description="Tuenti Challenge 2020 - Problem 12")
args = parser.parse_args()

contents_m1 = open('plaintext1.txt', 'rb').read()
contents_m2 = open('plaintext2.txt', 'rb').read()
contents_c1 = open('ciphered1.txt', 'rb').read()
contents_c2 = open('ciphered2.txt', 'rb').read()

pubkeys = [3, 5, 17, 257, 65537]

for byte_order in ['little', 'big']:
    m1 = int.from_bytes(contents_m1, byteorder=byte_order)
    m2 = int.from_bytes(contents_m2, byteorder=byte_order)
    c1 = int.from_bytes(contents_c1, byteorder=byte_order)
    c2 = int.from_bytes(contents_c2, byteorder=byte_order)

    print('m1:', m1)
    print('m2:', m2)
    print('c1:', c1)
    print('c2:', c2)

    for d in pubkeys:
        print('\n\nbyte order', byte_order, 'pubkey', d)
        n1 = pow(gmpy2.mpz(m1), d) - c1
        print('#n1', len(n1))
        n2 = pow(gmpy2.mpz(m2), d) - c2
        print('#n2', len(n2))
        my_gcd = gmpy2.gcd(n1, n2)
        print('gcd', my_gcd)