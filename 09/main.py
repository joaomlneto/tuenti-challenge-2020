#!/usr/bin/env python3

import argparse
import icu
import os
import re
import sys

parser = argparse.ArgumentParser(description="Tuenti Challenge 2020 - Problem 09")
parser.add_argument("-m", "--message", dest="message", type=str)
parser.add_argument("-c", "--ciphertext", dest="ciphertext", type=str)
args = parser.parse_args()

#key = [4, 0, 6, 1, 4, 1, 7, 8, 1, 6, 5, 7, 8, 0, 9, 2, 3, 1, 1, 1, 2, 2, 3]
key = '\x04\x00\x06\x01\x04\x01\x07\x08\x01\x06\x05\x07\x08\x00\x09\x02\x03\x01\x01\x01\x02\x02\x03'

def encrypt(key, msg):
    print('key', 'len=%d' % len(key), key)
    print('msg', 'len=%d' % len(msg), msg)
    crpt_msg = ''
    for i in range(0, len(msg)):
        c        = msg[i]
        asc_chr  = ord(c)
        key_pos  = len(key) - 1 - i
        key_char = key[key_pos]
        crpt_chr = asc_chr ^ ord(key_char)
        hx_crpt_chr = hex(crpt_chr)[2:]
        crpt_msg += hx_crpt_chr
        print('msg[%02d] = \'%s\' (%s)\t' % (i, c, hex(asc_chr)), \
              'key[%02d] = %s\t' % (key_pos, hex(ord(key_char))), \
              'ciphertext[%02d] = %s' % (i, hx_crpt_chr))
    return crpt_msg

def decrypt(key, ciphertext):
    print('key', 'len=%d' % len(key), key)
    print('ciphertext', 'len=%d' % len(ciphertext), ciphertext)
    msg = list("?" * len(key))
    for i in range(0, len(key)):
        c = int(ciphertext[2*i:2*i+2], 16)
        key_byte = ord(key[len(key) - 1 - i])
        msg[i] = chr(c ^ key_byte)
        print(hex(c), hex(key_byte), msg[i])
    return "".join(msg)


def find_key(msg, ciphertext):
    print('message', 'len=%d' % len(msg), msg)
    print('ciphertext', 'len=%d' % len(ciphertext), ciphertext)
    key = list("?" * len(msg))
    print(key)
    for i in range(0, len(msg)):
        msgchar = ord(msg[i])
        cipherchar = int(ciphertext[2*i:2*i+2], 16)
        keychar = cipherchar ^ msgchar
        print('msgchar', msg[i], 'ascii', hex(msgchar), 'cipherchar:', hex(cipherchar), 'keychar', hex(keychar))
        key[len(key)-1-i] = keychar
    return key



if args.message and args.ciphertext:
    print('recovering key from message and ciphertext...')
    key = find_key(args.message, args.ciphertext)
    print('key:', key)
elif args.message:
    print('encoding message using key...')
    ciphertext = encrypt(key, args.message)
    print('ciphertext:', ciphertext)
elif args.ciphertext:
    print('decoding ciphertext using key...')
    message = decrypt(key, args.ciphertext)
    print('message', message)
else:
    print('please provide at least one argument :-)')
