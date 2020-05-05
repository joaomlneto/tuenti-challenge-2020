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

# probably overkill, but this is the closed form of the function.
# it will spit out how many toilet paper rolls we need to build a
# center tower of height 'h' and an area of 1x1.
def required_rolls_for_height(h):
    assert h >= 3
    return int(round((16*(h**3)/3) - 20*(h**2) + (8*(h-3)*h) + ((71*h)/3) + 8))

# this is how much volume is on a given line/column
# (excluding central tower). that is, how many rolls
# are next to the tower in a given line/column
def volume_of_cut(h):
    return 2 * ((h-2)**2 + 2*(h-2))

# this will give you the required amount of rolls to build
# a fortress with the specified dimensions of the central tower
def required_rolls_for_fortress(h, w, l):
    return required_rolls_for_height(h) + \
           (w + l - 2) * volume_of_cut(h) + \
           (w * l - 1) * h

# find what is the tallest you can build the tower
# returns the max height for a given number of rolls
def find_height(max_rolls):
    if max_rolls < 43: return 'IMPOSSIBLE'
    h = 3
    # find the right ballpark first
    while required_rolls_for_height(h) <= max_rolls:
        h *= 10
    h = max(3, h/10)
    # find the actual value
    while required_rolls_for_height(h) <= max_rolls:
        h += 1
    return h - 1

# try to use the most rolls by maximizing the area
# of the central tower. returns the number of rolls
# that can be used.
def find_rolls(height, max_rolls):
    width = 1
    # find largest square tower
    while required_rolls_for_fortress(height, width + 1, width + 1) <= max_rolls:
        width += 1
    # check if we can make it a rectangle
    length = width
    if required_rolls_for_fortress(height, width, width + 1) <= max_rolls:
        length += 1
    # return the number of rolls we can use!
    return required_rolls_for_fortress(height, width, length)


def find_area_square(h, max_rolls):
    w = 1
    while required_rolls_for_fortress(h, w, w) <= max_rolls:
        w += 1
    return w

with open(args.filename, 'r') as file:
    num_cases = int(next(file))
    for i in range(0, num_cases):
        print('Case #%d: ' % (i+1), end='')
        available_rolls = int(next(file))
        height = find_height(available_rolls)
        if (height == 'IMPOSSIBLE'):
            print('IMPOSSIBLE')
        else:
            rolls = find_rolls(height, available_rolls)
            print('%d %d' % (height, rolls))
