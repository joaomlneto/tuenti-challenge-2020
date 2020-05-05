#!/usr/bin/env python3

import argparse
import icu
import os
import re
import sys

parser = argparse.ArgumentParser(description="Tuenti Challenge 2020 - Problem 03")
parser.add_argument("-f", "--file", dest="filename", type=str,
                    help="the text file to analyze", default='pg17013.txt')
parser.add_argument("-q", "--queries", dest="queries", type=str,
                    help="queries file", required=True)
args = parser.parse_args()

freqs = {}     # mapping word -> frequency
ranks = {}     # mapping word -> rank
word_rank = [] # mapping rank -> (frequency, word)

collator = icu.Collator.createInstance(icu.Locale('UTF-8'))

# compute how often each word appears
with open(args.filename, 'r') as file:
    for line in file:
        # convert all words to lowercase
        line = line.lower()
        # only consider a few letters
        line = re.sub("[^a-zñáéíóúü]", ' ', line);
        #print(line.rstrip())
        for word in line.split():
            # discard words with fewer than 3 characters
            if (len(word) < 3): continue
            freqs[word] = freqs.get(word, 0) + 1

# compute rankings by their frequency
for key, value in freqs.items():
    word_rank.append((value, key))
word_rank.sort(key = lambda x: (-x[0], x[1]))

# generate a word -> ranking mapping
for rank, word_freq in enumerate(word_rank):
    ranks[word_freq[1]] = rank + 1

# cycle through the queries
with open(args.queries, 'r') as file:
    num_queries = int(next(file))
    for query_num in range(0, num_queries):
        query = next(file).strip()
        # rank queries
        try:
            rank = int(query)
            word = word_rank[rank-1][1]
            print("Case #%d: %s %d" % (query_num + 1, word, freqs[word]))
        # word queries
        except ValueError:
            print("Case #%d: %d #%d" % (query_num + 1, freqs[query], ranks[query]))
