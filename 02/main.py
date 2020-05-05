#!/usr/bin/env python3

import argparse
import os
import sys

parser = argparse.ArgumentParser(description="Tuenti Challenge 2020 - Problem 02")
parser.add_argument("-f", "--file", dest="filename", type=str,
                    help="file to open", required=True)
args = parser.parse_args()

with open(args.filename) as f:
    num_cases = int(next(f))
    # iterate through all cases
    for case in range(0, num_cases):
        num_matches = int(next(f))
        players = set()
        losers = set()

        # iterate through all matches in a case
        for match in range(0, num_matches):
            playerA, playerB, result = [int(x) for x in next(f).split()]
            players.add(playerA)
            players.add(playerB)
            if (result == 1): losers.add(playerB)
            else: losers.add(playerA)

        winner = players.difference(losers)
        assert(len(winner) == 1);
        print("Case #%d: %d" % (case + 1, winner.pop()))