#!/usr/bin/env python3

import argparse
import icu
import os
import re
import sys

parser = argparse.ArgumentParser(description="Tuenti Challenge 2020 - Problem 10")
args = parser.parse_args()

# zombie bought 119 brains, apparently. hungry fella.
def is_number_of_brains(n):
    return n % 2 == 1 and n % 3 == 2 and n % 4 == 3 and n % 5 == 4 and n % 6 == 5 and n % 7 == 0
n = 7
while not is_number_of_brains(n): n += 7
print('number of brains:', n)

# shiloh: i bruteforced the robot error code -- ended up being 242
for i in range(0, 256):
    print("🗣 %d | /home/castle/🚪/🚪107/🤖" % i)

# Joey ghost: just ls -la (show hidden files) to see the ring

# vampire: the rhyme is written in the toilet paper in the bathroom

# genie: wake him up with ctrl-Z instead of ctrl-C

# ladybird: its in the hole
# just grab hole/ladybird: ✋ 🕳/🐞
# https://emojipedia.org/lady-beetle/
# give it back and...
# PetsAreNotAllowedInVillaFeristela